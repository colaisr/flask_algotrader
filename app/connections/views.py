import json
import ssl
from urllib.request import urlopen

import certifi
from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    url_for
)
from flask_login import login_required, current_user
from datetime import datetime

from sqlalchemy import text, desc

from app import db, csrf
from app.email import send_email

from app.models import (
    User, Connection, Report,
    Position, ClientCommand, UserSetting,
    TickerData, Candidate, TelegramSignal
)
from app.models.fgi_score import Fgi_score
from app.telegram.signal_notify import send_telegram_signal_message

from app.research import yahoo_research as yahoo

connections = Blueprint('connections', __name__)


@csrf.exempt
@connections.route('/logconnection', methods=['POST'])
def logconnection():
    request_data = request.get_json()
    logged_user = request_data["user"]
    user = User.query.filter_by(email=logged_user).first()
    if user is not None:
        c = Connection()
        c.email = logged_user
        now = datetime.utcnow()
        c.reported_connection = now
        c.log_connection()
        return "Application launch for " + logged_user + " is logged."
    else:
        return "The user configured is not found on Server the connection is not logged"


def filter_add_data(related_tds, logged_user, filters=None):
    if filters is None:
        user_settings = UserSetting.query.filter_by(email=logged_user).first()

        if user_settings.algo_apply_algotrader_rank:
            algo_ranks = list(filter(
                lambda
                    td: td.algotrader_rank is not None and td.algotrader_rank >= user_settings.algo_min_algotrader_rank,
                related_tds))
        else:
            algo_ranks = related_tds

        if user_settings.algo_apply_min_underprice:
            filtered_underprice = list(
                filter(lambda
                           td: td.under_priced_pnt is not None and td.under_priced_pnt >= user_settings.algo_min_underprice,
                       algo_ranks))
        else:
            filtered_underprice = algo_ranks

        if user_settings.algo_apply_min_momentum:
            filtered_momentum = list(
                filter(lambda
                           td: td.twelve_month_momentum is not None and td.twelve_month_momentum >= user_settings.algo_min_momentum,
                       filtered_underprice))
        else:
            filtered_momentum = filtered_underprice

        if user_settings.algo_apply_min_beta:
            filtered_beta = list(
                filter(lambda td: td.beta is not None and td.beta >= user_settings.algo_min_beta, filtered_momentum))
        else:
            filtered_beta = filtered_momentum

        if user_settings.algo_apply_max_intraday_drop_percent:
            filtered_max_intraday_drop = list(
                filter(lambda
                           td: td.max_intraday_drop_percent is not None and td.max_intraday_drop_percent < user_settings.algo_max_intraday_drop_percent,
                       filtered_beta))
        else:
            filtered_max_intraday_drop = filtered_beta
    else:
        algo_ranks = list(filter(
            lambda td: td.algotrader_rank is not None and td.algotrader_rank >= filters['algo_min_algotrader_rank'],
            related_tds))

        filtered_underprice = list(
            filter(
                lambda td: td.under_priced_pnt is not None and td.under_priced_pnt >= filters['algo_min_underprice'],
                algo_ranks))

        filtered_momentum = list(
            filter(lambda
                       td: td.twelve_month_momentum is not None and td.twelve_month_momentum >= filters[
                'algo_min_momentum'],
                   filtered_underprice))

        filtered_beta = list(
            filter(lambda td: td.beta is not None and td.beta >= filters['algo_min_beta'], filtered_momentum))

        filtered_max_intraday_drop = list(
            filter(lambda
                       td: td.max_intraday_drop_percent is not None and td.max_intraday_drop_percent < filters[
                'algo_max_intraday_drop_percent'],
                   filtered_beta))

    return filtered_max_intraday_drop


def sort_by_parameter_desc(obj, prop):
    return sorted(obj, key=lambda x: x[prop], reverse=True)


def sort_by_parameter_asc(obj, prop):
    return sorted(obj, key=lambda x: x[prop], reverse=False)


def sort_candidates(cand_dictionaries):
    sorted_momentum = sort_by_parameter_desc(cand_dictionaries, 'twelve_month_momentum')
    sorted_underprice = sort_by_parameter_desc(sorted_momentum, 'under_priced_pnt')
    sorted_yahooo = sort_by_parameter_asc(sorted_underprice, 'yahoo_rank')
    sorted_tiprank = sort_by_parameter_desc(sorted_yahooo, 'tipranks')
    return sorted_tiprank


def retrieve_user_candidates(user):
    requested_for_user = user
    requested_candidates = get_requested_candidates(requested_for_user)
    requested_candidates = filter_add_data(requested_candidates, requested_for_user)
    # requested_candidates.sort(key=sort_by_tiprank)
    # requested_candidates=requested_candidates[:85]    #trader station allow to track only 100
    cand_dictionaries = []
    for c in requested_candidates:
        cand_dictionaries.append(c.toDictionary())
    sorted_list = sort_candidates(cand_dictionaries)
    return sorted_list


def get_requested_candidates(user):
    user_candidates = Candidate.query.filter_by(email=user, enabled=True).all()
    user_settings = UserSetting.query.filter_by(email=user).first()

    if user_settings.server_use_system_candidates:
        admin_candidates = Candidate.query.filter_by(email='support@algotrader.company', enabled=True).all()
        for uc in user_candidates:
            for ac in admin_candidates:
                if ac.ticker == uc.ticker:
                    break
            else:
                admin_candidates.append(uc)
        requested_candidates = admin_candidates
    else:
        requested_candidates = user_candidates

    query_text = "select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    uniq_tickers_data = db.session.query(TickerData).from_statement(text(query_text)).all()

    related_tds = []
    for c in requested_candidates:
        adding = list(filter(lambda td: td.ticker == c.ticker, uniq_tickers_data))
        if len(adding) == 0:
            pass
        else:
            related_tds.append(adding[0])
    return related_tds


@csrf.exempt
@connections.route('/filter_candidates_data_ajax', methods=['POST'])
@login_required
def filter_candidates_data_ajax():
    related_tds = get_requested_candidates(current_user.email)
    algo_min_underprice = float(request.form['filtered_underprice'])
    algo_min_algotrader_rank = float(request.form['algo_ranks'])
    algo_min_momentum = float(request.form['filtered_momentum'])
    algo_min_beta = float(request.form['filtered_beta'])
    algo_max_intraday_drop_percent = float(request.form['filtered_max_intraday_drop'])

    filters = {
        'algo_min_underprice': algo_min_underprice,
        'algo_min_algotrader_rank': algo_min_algotrader_rank,
        'algo_min_momentum': algo_min_momentum,
        'algo_min_beta': algo_min_beta,
        'algo_max_intraday_drop_percent': algo_max_intraday_drop_percent
    }

    algo_ranks = list(
        filter(lambda td: td.algotrader_rank != None and td.algotrader_rank >= algo_min_algotrader_rank, related_tds))
    filtered_underprice = list(
        filter(lambda td: td.under_priced_pnt != None and td.under_priced_pnt >= algo_min_underprice, related_tds))
    filtered_momentum = list(
        filter(lambda td: td.twelve_month_momentum != None and td.twelve_month_momentum >= algo_min_momentum,
               related_tds))
    filtered_beta = list(filter(lambda td: td.beta != None and td.beta >= algo_min_beta, related_tds))
    filtered_max_intraday_drop = list(filter(lambda
                                                 td: td.max_intraday_drop_percent != None and td.max_intraday_drop_percent < algo_max_intraday_drop_percent,
                                             related_tds))
    total = filter_add_data(related_tds, current_user.email, filters)
    result = {
        'algo_ranks': len(algo_ranks),
        'filtered_underprice': len(filtered_underprice),
        'filtered_momentum': len(filtered_momentum),
        'filtered_beta': len(filtered_beta),
        'filtered_max_intraday_drop': len(filtered_max_intraday_drop),
        'total': len(total)
    }
    return json.dumps(result)


def sort_by_tiprank(e):
    return e.tipranks


def check_signal_for_target_riched(s, bid_price):
    if bid_price >= s.target_price:
        s.target_met = datetime.utcnow()
        delta = s.target_met - s.received
        s.days_to_get = delta.days
        # profit yet to be measured
        s.profit_percent = (bid_price - s.signal_price) / bid_price * 100
        s.update_signal()
        send_telegram_signal_message("Confirmation for : " + str(s.id) + "\n" +
                                     s.ticker + " reached target of " + str(s.target_price) + "\n" +
                                     "in " + str(s.days_to_get) + " days, with profit of " + str(round(s.profit_percent, 2)) + " %"+ "\n" +
                                    "by https://www.algotrader.company"

                                     )

    pass


@connections.route('signals_check', methods=['GET'])
@csrf.exempt
def signals_check():
    signals = TelegramSignal.query.filter_by(target_met=None).all()
    all_reports = Report.query.all()
    all_prices_reported = {}
    for r in all_reports:
        candidates_live = json.loads(r.candidates_live_json)
        for k, c in candidates_live.items():
            all_prices_reported[c['Stock']] = c['Bid']
    for s in signals:
        if s.ticker in all_prices_reported:
            if s.target_price is not None:
                check_signal_for_target_riched(s, all_prices_reported[s.ticker])

    return "Signals checked"


def process_signals_candidates(ready_data):
    for k,v in ready_data.items():
        if v['current_price']<=v['buying_target_price_fmp']:
            rank=str(v['algotrader_rank'])
            under_priced=str(v['under_priced_pnt'])
            target=str(v['target_mean_price'])
            ticker = k
            signal = TelegramSignal.query.filter_by(target_met=None, ticker=ticker).order_by(
                TelegramSignal.id.desc()).first()
            if signal is not None:
                signal_date = signal.received.date()
                today = datetime.utcnow().date()
                if signal_date != today:     #there was no same signal today
                    signal = TelegramSignal()
                    signal.ticker = ticker
                    signal.received = datetime.today().date()
                    signal.transmitted = True
                    signal.signal_price = v['current_price']
                    try:
                        signal.target_price = target
                        added = signal.add_signal()
                        if added:
                            send_telegram_signal_message(str(signal.id) + "\n" +
                                                         "Time to buy: " + signal.ticker + "\n" +
                                                         "it crossed the trigger of " + str(
                                round(v['buying_target_price_fmp'], 2)) + " USD \n" +
                                                         "Algotrader Rank: " + str(rank) + "\n" +
                                                         "Expected to reach the target of: " + str(target) + " USD"+"\n" +
                                                         "https://www.algotrader.company/candidates/info/"+signal.ticker
                                                         )
                    except:
                        print("Error in signal for : " + signal.ticker)



@connections.route('signals_create', methods=['GET'])
@csrf.exempt
def signals_create():
    minimal_rank=9.1
    url='https://colak.eu.pythonanywhere.com/data_hub/current_market_operation/'   #checking market is open
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    data = json.loads(data)
    if data['isTheStockMarketOpen']==True:
        query_text=f"SELECT a.* FROM Tickersdata a JOIN (SELECT ticker, MAX(updated_server_time) AS updated_server_time FROM Tickersdata GROUP BY ticker) b ON b.ticker=a.ticker AND b.updated_server_time=a.updated_server_time WHERE a.algotrader_rank >= "+str(minimal_rank)+" AND a.under_priced_pnt > 0"
        relevant_tickers = db.session.query(TickerData).from_statement(text(query_text)).all()
        tickers_string=''
        for t in relevant_tickers:
            tickers_string+=','+t.ticker
        tickers_string=tickers_string[1:]
        url='https://colak.eu.pythonanywhere.com/data_hub/current_stock_price_short/'+tickers_string
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        prices=json.loads(data)
        ready_data={}
        for t in relevant_tickers:
            filtered = filter(lambda price: price["symbol"] == t.ticker, prices)
            filtered_price=list(filtered)
            if len(filtered_price)>0 and t.buying_target_price_fmp is not None:   #only those who have prices
                price=filtered_price[0]
                ready_data[t.ticker]={'algotrader_rank':t.algotrader_rank,
                                      'buying_target_price_fmp':t.buying_target_price_fmp,
                                      'under_priced_pnt':t.under_priced_pnt,
                                      'target_mean_price':t.target_mean_price,
                                      'current_price':price['price']}
        process_signals_candidates(ready_data)
        return "Signals checked"
    else:
        return "Market is closed - not checking signals"


def check_for_signals(candidates_live_json):
    candidates_live = json.loads(candidates_live_json)
    for k, v in candidates_live.items():
        if v['Ask'] < v['target_price'] and v['Ask'] != -1:
            ticker = v['Stock']
            signal = TelegramSignal.query.filter_by(target_met=None, ticker=ticker).order_by(
                TelegramSignal.id.desc()).first()
            if signal is not None:
                signal_date = signal.received.date()
                today = datetime.utcnow().date()
                if signal_date != today:     #there was no same signal today
                    signal = TelegramSignal()
                    ticker_data = TickerData.query.filter_by(ticker=v['Stock']).order_by(
                        TickerData.updated_server_time.desc()).first()
                    signal.ticker = v['Stock']
                    signal.received = datetime.today().date()
                    signal.transmitted = True
                    signal.signal_price = v['Ask']
                    try:
                        if ticker_data.algotrader_rank >= 9.3:
                            if ticker_data.target_mean_price is None:
                                signal.target_price = 0
                            else:
                                signal.target_price = ticker_data.target_mean_price
                            added = signal.add_signal()
                            if added:
                                send_telegram_signal_message(str(signal.id) + "\n" +
                                                             "Time to buy: " + signal.ticker + "\n" +
                                                             "it crossed the trigger of " + str(
                                    round(v['target_price'], 2)) + " USD \n" +
                                                             "Algotrader Rank: " + str(ticker_data.algotrader_rank) + "\n" +
                                                             "Expected to reach the target of: " + str(
                                    ticker_data.target_mean_price) + " USD"
                                                             )
                    except:
                        print("Error in signal for : " + signal.ticker)
                        print(ticker_data)


@csrf.exempt
@connections.route('/postreport', methods=['POST'])
def logreport():
    request_data = request.get_json()
    logged_user = request_data["user"]
    user = User.query.filter_by(email=logged_user).first()
    if user is not None:
        report = Report()
        report.email = logged_user
        report.report_time = datetime.fromisoformat(request_data["report_time"])
        report.report_time = datetime.utcnow()
        report.remaining_trades = request_data["remaining_trades"]
        report.open_positions_json = request_data["open_positions"]
        report.open_orders_json = request_data["open_orders"]
        report.candidates_live_json = request_data["candidates_live"]
        report.all_positions_value = request_data["all_positions_value"]
        report.net_liquidation = request_data["net_liquidation"]
        report.remaining_sma_with_safety = request_data["remaining_sma_with_safety"]
        report.excess_liquidity = request_data["excess_liquidity"]
        report.dailyPnl = request_data["dailyPnl"]
        report.api_connected = request_data["api_connected"]
        report.last_worker_execution = datetime.fromisoformat(request_data["last_worker_run"])
        report.market_time = datetime.fromisoformat(request_data["market_time"])
        report.market_state = request_data["market_state"]
        report.started_time = datetime.fromisoformat(request_data["started_time"])
        report.market_data_error = request_data["market_data_error"]
        report.client_version = request_data["client_version"]
        report.update_report()

        if report.api_connected:
            if report.market_state == "Open":  # can be none .... in not taken from api...tws not yet connected on first run
                check_stop_loss(logged_user, report.net_liquidation)
                check_if_market_fall(logged_user)
                #check_for_signals(report.candidates_live_json)

        return "Report snapshot stored at server"
    else:
        return "The user configured is not found on Server the report is not logged"


def retrieve_user_positions(logged_user):
    open_positions = Position.query.filter_by(last_exec_side='BOT', email=logged_user)
    open_positions_dictionaries = []
    for c in open_positions:
        open_positions_dictionaries.append(c.toDictionary())
    return open_positions_dictionaries


@csrf.exempt
@connections.route('/getcommand', methods=['POST'])
def get_command():
    request_data = request.get_json()
    logged_user = request_data["user"]
    user = User.query.filter_by(email=logged_user).first()
    if user is not None:
        response = {}
        client_command = ClientCommand.query.filter_by(email=logged_user).first()
        market_emotion = db.session.query(Fgi_score).order_by(Fgi_score.score_time.desc()).first()
        response['command'] = client_command.command
        response['candidates'] = retrieve_user_candidates(logged_user)
        response['open_positions'] = retrieve_user_positions(logged_user)
        response['market_emotion'] = market_emotion.fgi_value
        if client_command.command == 'restart_worker':
            client_command.set_run_worker()
        elif client_command.command == 'close_all_positions':
            client_command.set_run_worker()
        return response
    else:
        return "The user configured for Get Command is not found on Server"


@csrf.exempt
@connections.route('logrestartrequest/', methods=['POST'])
def log_restart_request():
    logged_user = request.form['usersemail']
    from_admin = request.form['fromadmin']
    url_redirect = 'admin.users_monitor' if from_admin == "1" else 'userview.traderstationstate'
    client_command = ClientCommand.query.filter_by(email=logged_user).first()
    client_command.set_restart()
    flash('Restart request logged', 'success')
    return redirect(url_for(url_redirect))


@csrf.exempt
@connections.route('restart_all_stations', methods=['POST'])
def restart_all_stations():
    clients = ClientCommand.query.all()
    for c in clients:
        c.set_restart()
    return "all stations booked to restart"


def check_stop_loss(logged_user, net_liquidation):
    stop_loss = UserSetting.query.filter_by(email=logged_user).first().algo_portfolio_stoploss
    if net_liquidation <= stop_loss:
        client_command = ClientCommand.query.filter_by(email=logged_user).first()
        client_command.set_close_all_positions()


def check_if_market_fall(logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    user = User.query.filter_by(email=logged_user).first()
    if user_settings.algo_sell_on_swan:
        snp = yahoo.get_current_snp_change_percents()
        if user_settings.algo_positions_for_swan >= snp:
            # more than 3 positions closed same day on profit negative - stop buying option and notify
            user_settings = UserSetting.query.filter_by(email=logged_user).first()
            user_settings.algo_allow_buy = False
            user_settings.update_user_settings()
            send_email(recipient=logged_user,
                       user=user,
                       subject='Algotrader: Black Swan is suspected!',
                       template='account/email/black_swan')

            client_command = ClientCommand.query.filter_by(email=logged_user).first()
            client_command.set_close_all_positions()


def notify_open(position, logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    if user_settings.notify_buy:
        send_email(recipient=logged_user,
                   subject='Algotrader: new position is open for ' + position.ticker,
                   template='account/email/position_open',
                   position=position)


def notify_closed(position, logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()

    if user_settings.notify_sell:
        if position.profit > 0:
            text_for_message = 'Algotrader: closed position for ' + position.ticker + " with Profit"
        else:
            text_for_message = 'Algotrader: closed position for ' + position.ticker + "with Loss"
        send_email(recipient=logged_user,
                   subject=text_for_message,
                   template='account/email/position_close',
                   position=position)


@csrf.exempt
@connections.route('/postexecution', methods=['POST'])
def postexecution():
    request_data = request.get_json()
    logged_user = request_data["user"]
    symbol = request_data["symbol"]
    shares = request_data["shares"]
    price = request_data["price"]
    side = request_data["side"]
    exec_id=request_data["exec_id"]
    reported_time = json.loads(request_data['time'])
    time = datetime.fromisoformat(reported_time)

    user = User.query.filter_by(email=logged_user).first()
    if user is not None:
        position = Position()
        position.ticker = symbol
        position.email = logged_user
        position.stocks = shares
        position.last_exec_side = side
        if side == 'BOT':
            position.open_price = price
            position.opened = time
            position.exec_id_buy=str(exec_id)
        else:
            position.close_price = price
            position.closed = time
            position.exec_id_sld=str(exec_id)

        result, np = position.update_position()

        if result == "new_sell":
            # check_if_market_fall(logged_user)
            notify_closed(np, logged_user)
        elif result == "new_buy":
            notify_open(np, logged_user)

        return "Execution for " + logged_user + " stored at server."
    else:
        return "The user configured is not found on Server the execution is not logged"
