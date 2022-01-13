import json
import app.generalutils as general
import ssl
import time
import sys
import app.enums as enum
from urllib.request import urlopen

import certifi
from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    url_for, render_template
)
from flask_login import login_required, current_user
from datetime import datetime

from sqlalchemy import text, desc

from app import db, csrf
from app.email import send_email
from app.api_service import api_service

from app.models import (
    User, Connection, Report,
    Position, ClientCommand, UserSetting,
    TickerData, Candidate, TelegramSignal, Notification, ProcessStatus, NotificationProcess
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
    return sorted(obj, key=lambda x: 0 if x[prop] is None else x[prop], reverse=True)


def sort_by_parameter_asc(obj, prop):
    return sorted(obj, key=lambda x: 0 if x[prop] is None else x[prop], reverse=False)


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
    candidates = Candidate.query.filter_by(enabled=True).all()
    cand_dictionaries = []
    for c in requested_candidates:
        item = c.toDictionary()
        cand = next(item for item in candidates if item.ticker == c.ticker)
        item['website'] = cand.website
        item['company_name'] = cand.company_name
        cand_dictionaries.append(item)
    sorted_list = sort_candidates(cand_dictionaries)
    return sorted_list


def get_requested_candidates(user):
    user_candidates = Candidate.query.filter_by(email=user, enabled=True).all()
    user_settings = UserSetting.query.filter_by(email=user).first()

    if user_settings.server_use_system_candidates:
        admin_candidates = Candidate.query.filter_by(email='support@stockscore.company', enabled=True).all()
        tickers_lst = [ac.ticker for ac in admin_candidates]
        uc = [uc for uc in user_candidates if uc.ticker not in tickers_lst]
        if len(uc) > 0:
            tickers_lst.extend([t.ticker for t in uc])
        requested_candidates = tickers_lst
    else:
        requested_candidates = [uc.ticker for uc in user_candidates]

    query_text = f"select a.* from Tickersdata a " \
                 f"join (  select Tickersdata.`ticker`, " \
                 f"max(Tickersdata.`updated_server_time`) as updated_server_time  " \
                 f"from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` " \
                 f"JOIN Candidates c ON c.`ticker`=a.`ticker` " \
                 f"and b.`updated_server_time`=a.`updated_server_time`"

    # uniq_tickers_data_res = db.engine.execute(text(query_text))
    # uniq_tickers_data = [dict(r.items()) for r in uniq_tickers_data_res]

    uniq_tickers_data = db.session.query(TickerData).from_statement(text(query_text)).all()

    related_tds = [x for x in uniq_tickers_data if x.ticker in requested_candidates]

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
                                     "in " + str(s.days_to_get) + " days, with profit of " + str(
            round(s.profit_percent, 2)) + " %" + "\n" +
                                     "by https://www.stockscore.company"
                                     )
        # print("Confirmation for : " + str(s.id) + "\n" +
        #                              s.ticker + " reached target of " + str(s.target_price) + "\n" +
        #                              "in " + str(s.days_to_get) + " days, with profit of " + str(round(s.profit_percent, 2)) + " %"+ "\n" +
        #                             "by https://www.stockscore.company")

    pass


@connections.route('signals_check', methods=['GET'])
@csrf.exempt
def signals_check():
    signals = TelegramSignal.query.filter_by(target_met=None).all()
    all_prices_reported = {}

    tickers_string = ''
    tickers_list = []
    for t in signals:
        tickers_list.append(t.ticker)
    tickers_list = list(set(tickers_list))
    for s in tickers_list:
        tickers_string += ',' + s
    tickers_string = tickers_string[1:]
    url = 'https://colak.eu.pythonanywhere.com/data_hub/current_stock_price_short/' + tickers_string
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    prices = json.loads(data)
    prices_dict = {}
    for p in prices:
        prices_dict[p['symbol']] = p['price']
    for s in signals:
        if s.ticker in prices_dict:
            if s.target_price is not None:
                check_signal_for_target_riched(s, prices_dict[s.ticker])

    return "Signals checked"


def process_signals_candidates(ready_data):
    for k, v in ready_data.items():
        # testing
        # ticker = k
        # target = str(v['target_mean_price'])
        # signal = TelegramSignal()
        # signal.ticker = ticker
        # signal.received = datetime.today().date()
        # signal.transmitted = True
        # signal.signal_price = v['current_price']
        # signal.target_price = target
        # added = signal.add_signal()
        # end of testing

        if v['current_price'] <= v['buying_target_price_fmp']:
            rank = str(v['algotrader_rank'])
            under_priced = str(v['under_priced_pnt'])
            target = str(v['target_mean_price'])
            ticker = k
            signal = TelegramSignal.query.filter_by(target_met=None, ticker=ticker).order_by(
                TelegramSignal.id.desc()).first()
            if signal is not None:
                signal_date = signal.received.date()
                today = datetime.utcnow().date()
                if signal_date != today:  # there was no same signal today
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
                                                         "Stock Score Rank: " + str(rank) + "\n" +
                                                         "Expected to reach the target of: " + str(
                                target) + " USD" + "\n" +
                                                         "https://www.stockscore.company/candidates/info/" + signal.ticker
                                                         )
                    except:
                        print("Error in signal for : " + signal.ticker)


@connections.route('signals_create', methods=['GET'])
@csrf.exempt
def signals_create():
    minimal_rank = 9.1
    # url = 'https://colak.eu.pythonanywhere.com/data_hub/current_market_operation/'  # checking market is open
    # context = ssl.create_default_context(cafile=certifi.where())
    # response = urlopen(url, context=context)
    # data = response.read().decode("utf-8")
    # data = json.loads(data)
    data = api_service.is_market_open_api()
    data = json.loads(data)
    if data['isTheStockMarketOpen'] == True:
        query_text = f"SELECT a.* FROM Tickersdata a JOIN (SELECT ticker, MAX(updated_server_time) AS updated_server_time FROM Tickersdata GROUP BY ticker) b ON b.ticker=a.ticker AND b.updated_server_time=a.updated_server_time WHERE a.algotrader_rank >= " + str(
            minimal_rank) + " AND a.under_priced_pnt > 0"
        relevant_tickers = db.session.query(TickerData).from_statement(text(query_text)).all()
        tickers_string = ''
        for t in relevant_tickers:
            tickers_string += ',' + t.ticker
        tickers_string = tickers_string[1:]
        url = 'https://colak.eu.pythonanywhere.com/data_hub/current_stock_price_short/' + tickers_string
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        prices = json.loads(data)
        ready_data = {}
        for t in relevant_tickers:
            filtered = filter(lambda price: price["symbol"] == t.ticker, prices)
            filtered_price = list(filtered)
            if len(filtered_price) > 0 and t.buying_target_price_fmp is not None:  # only those who have prices
                price = filtered_price[0]
                ready_data[t.ticker] = {'algotrader_rank': t.algotrader_rank,
                                        'buying_target_price_fmp': t.buying_target_price_fmp,
                                        'under_priced_pnt': t.under_priced_pnt,
                                        'target_mean_price': t.target_mean_price,
                                        'current_price': price['price']}
        process_signals_candidates(ready_data)
        return "Signals checked"
    else:
        return "Market is closed - not checking signals"


# def check_for_signals(candidates_live_json):
#     candidates_live = json.loads(candidates_live_json)
#     for k, v in candidates_live.items():
#         if v['Ask'] < v['target_price'] and v['Ask'] != -1:
#             ticker = v['Stock']
#             signal = TelegramSignal.query.filter_by(target_met=None, ticker=ticker).order_by(
#                 TelegramSignal.id.desc()).first()
#             if signal is not None:
#                 signal_date = signal.received.date()
#                 today = datetime.utcnow().date()
#                 if signal_date != today:     #there was no same signal today
#                     signal = TelegramSignal()
#                     ticker_data = TickerData.query.filter_by(ticker=v['Stock']).order_by(
#                         TickerData.updated_server_time.desc()).first()
#                     signal.ticker = v['Stock']
#                     signal.received = datetime.today().date()
#                     signal.transmitted = True
#                     signal.signal_price = v['Ask']
#                     try:
#                         if ticker_data.algotrader_rank >= 9.3:
#                             if ticker_data.target_mean_price is None:
#                                 signal.target_price = 0
#                             else:
#                                 signal.target_price = ticker_data.target_mean_price
#                             added = signal.add_signal()
#                             if added:
#                                 send_telegram_signal_message(str(signal.id) + "\n" +
#                                                              "Time to buy: " + signal.ticker + "\n" +
#                                                              "it crossed the trigger of " + str(
#                                     round(v['target_price'], 2)) + " USD \n" +
#                                                              "Algotrader Rank: " + str(ticker_data.algotrader_rank) + "\n" +
#                                                              "Expected to reach the target of: " + str(
#                                     ticker_data.target_mean_price) + " USD"
#                                                              )
#                     except:
#                         print("Error in signal for : " + signal.ticker)
#                         print(ticker_data)


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
                # check_if_market_fall(logged_user)
                # check_for_signals(report.candidates_live_json)

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
@connections.route('/get_fitered_candidates_for_user', methods=['GET'])
def get_fitered_candidates_for_user():
    # for traderstation
    user = request.args.get('user')
    candidates = retrieve_user_candidates(user)
    tickers_string = ''
    for t in candidates:
        tickers_string += t['ticker'] + ','
    data = api_service.current_stock_price(tickers_string)
    prices = json.loads(data)
    for cand in candidates:
        price = next(item for item in prices if item['symbol'] == cand['ticker'])
        cand['price'] = price['price']
    return render_template('partial/user_candidates.html', candidates=candidates)


@csrf.exempt
@connections.route('/get_favorites_for_user', methods=['GET'])
def get_favorites_for_user():
    # for traderstation
    user = request.args.get('user')
    candidates_o = Candidate.query.filter_by(email=user, enabled=True).all()
    candidates = []
    for c in candidates_o:
        candidates.append(c.to_dictionary())
    tickers_string = ''
    for t in candidates:
        tickers_string += t['ticker'] + ','
    # tickers_string = tickers_string[1:]
    url = 'https://colak.eu.pythonanywhere.com/data_hub/current_stock_price_full/' + tickers_string
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    prices = json.loads(data)
    total_today_change = 0
    total_complete_change = 0
    for cand in candidates:
        price = next(item for item in prices if item['symbol'] == cand['ticker'])
        cand['price'] = price['price']
        change = price['price'] - cand['price_added']
        change_percent = change / cand['price_added'] * 100
        cand['change_complete_percents'] = change_percent
        total_complete_change += change_percent
        cand['change_today_percents'] = price['changesPercentage']
        total_today_change += price['changesPercentage']

    return render_template('partial/user_favorites.html', candidates=candidates,
                           total_complete_change=total_complete_change, total_today_change=total_today_change)


@csrf.exempt
@connections.route('/get_positions_for_user', methods=['GET'])
def get_positions_for_user():
    # for traderstation
    user = request.args.get('user')
    settings = UserSetting.query.filter_by(email=current_user.email).first()
    report = Report.query.filter_by(email=current_user.email).first()
    use_margin = settings.algo_allow_margin
    report_interval = settings.server_report_interval_sec
    if report is None:
        open_positions = {}
        open_orders = {}
        candidates_live = {}
    else:
        report.reported_text = report.report_time.strftime("%d %b %H:%M:%S")
        if report.started_time is not None:
            report.started_time_text = report.started_time.strftime("%d %b %H:%M:%S")
        else:
            report.started_time_text = '---------------------'
        report.last_worker_execution_text = report.last_worker_execution.strftime("%H:%M:%S")
        report.market_time_text = report.market_time.strftime("%H:%M")
        report.dailyPnl = round(report.dailyPnl, 2)
        pnl_bg_box_color = 'bg-danger' if report.dailyPnl < 0 else 'bg-success'
        report.remaining_sma_with_safety = round(report.remaining_sma_with_safety, 2)

        open_positions = json.loads(report.open_positions_json)
        open_orders = json.loads(report.open_orders_json)
        report.all_positions_value = 0
        sectors_dict = {}
        for k, v in open_positions.items():
            position = Position.query.filter_by(email=current_user.email, last_exec_side='BOT', ticker=k).first()
            if position is not None:
                delta = datetime.today() - position.opened
                v['days_open'] = delta.days
            else:
                v['days_open'] = 0

            profit = v['UnrealizedPnL'] / v['Value'] * 100 if v['Value'] != 0 else 0
            v['profit_in_percents'] = profit
            if v['stocks'] != 0:
                report.all_positions_value += int(v['Value'])
                v['last_bid'] = v['Value'] / v['stocks']
            if profit > 0:
                v['profit_class'] = 'text-success'
                v['profit_progress_colour'] = 'bg-success'
                v['profit_progress_percent'] = profit / 6 * 100
            else:
                v['profit_class'] = 'text-danger'
                v['profit_progress_colour'] = 'bg-danger'
                v['profit_progress_percent'] = abs(profit / 10 * 100)

            candidate = Candidate.query.filter_by(ticker=k).first()
            sectors_dict[candidate.sector] = sectors_dict[candidate.sector] + int(
                v['Value']) if candidate.sector in sectors_dict.keys() else int(v['Value'])

        graph_sectors = []
        graph_sectors_values = []
        for sec, val in sectors_dict.items():
            graph_sectors.append(sec)
            graph_sectors_values.append(val)

        if not use_margin:
            report.excess_liquidity = round(report.net_liquidation - report.all_positions_value, 1)

        candidates_live = json.loads(report.candidates_live_json)
        for k, v in candidates_live.items():
            if 'target_price' not in v.keys():
                v['target_price'] = 0

        online = general.user_online_status(report.report_time, settings.station_interval_worker_sec)
        api_error = False if report.api_connected else True
    if report is not None:
        if report.net_liquidation != 0:
            report.pnl_percent = round(report.dailyPnl / report.net_liquidation * 100, 2)
        else:
            report.pnl_percent = 0
    return render_template('partial/user_positions.html',
                           graph_sectors=graph_sectors,
                           graph_sectors_values=graph_sectors_values,
                           online=online,
                           api_error=api_error,
                           report_interval=report_interval,
                           report_time=report.report_time,
                           open_positions=open_positions,
                           open_orders=open_orders,
                           report=report,
                           margin_used=use_margin,
                           pnl_bg_box_color=pnl_bg_box_color
                           )


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


@connections.route('market_fall_check', methods=['GET'])
@csrf.exempt
def check_if_market_fall():
    url = 'https://colak.eu.pythonanywhere.com/data_hub/current_snp/'  # checking market is open
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    data = json.loads(data)
    current_snp_change = data[0]['changesPercentage']
    print('snp fall checked current :' + str(current_snp_change))
    all_users = UserSetting.query.all()
    for us in all_users:
        if us.algo_sell_on_swan:
            minimal_intraday_allowed = us.algo_positions_for_swan
            if current_snp_change < minimal_intraday_allowed:
                last_notification = us.last_market_fall_notification
                if last_notification is not None:
                    last_notification = last_notification.date()
                today = datetime.utcnow().date()
                if last_notification != today:  # check if notification allready issued
                    us.algo_allow_buy = False
                    us.last_market_fall_notification = datetime.utcnow()
                    us.update_user_settings()
                    print('blackswan for '+us.email)
                    send_email(recipient=us.email,
                               user=us.email,
                               subject='StockScore: Market failed below ' + str(
                                   minimal_intraday_allowed) + '%  to ' + str(current_snp_change) + 'within a day',
                               template='account/email/black_swan')
            #enable after testing
                    client_command = ClientCommand.query.filter_by(email=us.email).first()
                    if client_command is not None:
                        client_command.set_close_all_positions()
                        print("blackswon notification was issued for"+us.email)
    print('The check is done.')
    return 'True'


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
            text_for_message = 'StockScore:Profit closed position for ' + position.ticker
        else:
            text_for_message = 'StockScore:Loss closed position for ' + position.ticker
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
    exec_id = request_data["exec_id"]
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
            position.exec_id_buy = str(exec_id)
        else:
            position.close_price = price
            position.closed = time
            position.exec_id_sld = str(exec_id)

        result, np = position.update_position()

        if result == "new_sell":
            # check_if_market_fall(logged_user)
            notify_closed(np, logged_user)
        elif result == "new_buy":
            notify_open(np, logged_user)

        return "Execution for " + logged_user + " stored at server."
    else:
        return "The user configured is not found on Server the execution is not logged"


@csrf.exempt
@connections.route('/notifications_process', methods=['GET'])
def notifications_process():
    start_time = datetime.now()
    print("****Starting notifications process  " + start_time.strftime("%d/%m/%Y %H:%M:%S") + "****")

    try:
        data = api_service.is_market_open_api()
        if data['isTheStockMarketOpen']:
            users = UserSetting.query.filter_by(notify_candidate_signal=1).all()
            update_process_status(0, len(users), 0, 0)

            error_status = 0

            p = 100 / len(users)
            min_step = 2

            update_times = []
            counter = 1
            percent = 2

            for u in users:
                try:
                    start_update_time = time.time()
                    print(f'Notifications for : {u} stamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
                    response = tickers_notifications(u.email)
                    end_update_time = time.time()
                    print(f"Updated stamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

                    if response["status"] == 0:
                        delta = end_update_time - start_update_time
                        update_times.append(delta)
                    else:
                        counter -= 1

                    if counter * p >= percent:
                        update_process_status(percent, len(users), counter - 1, 1)
                        percent += min_step
                except Exception as e:
                    print(f"Error in for cycle: {e}")
                    error_status = 1
                    counter -= 1
                counter += 1

            update_process_status(percent, len(users), counter - 1, 2)

            avg = sum(update_times) / len(update_times) if len(update_times) != 0 else 0
            end_time = datetime.now()
            print(f"***All notifications sended {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
            print("***Save last time update***")

            data = {
                "error_status": error_status,
                "start_time": start_time,
                "end_time": end_time,
                "num_of_users": len(users),
                "num_users_received": len(update_times),
                "avg_update_times": avg
            }
            try:
                response = save_process_data(data)
                print("***Date updated***")
            except Exception as e:
                print("Saving time update data failed. ", e)
            print("*************************************************")
        else:
            print("***** US market Closed *****")
    except Exception as e:
        print("Notifications process error. ", e)

    print("****Notifications process finished " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "****")
    return json.dumps({"status":"success"})


def update_process_status(percent, all_items, updated_items, status):
    try:
        process_status = ProcessStatus.query.filter_by(process_type=enum.ProcessType.NOTIFICATIONS.value).first()
        if process_status is None:
            process_status = ProcessStatus()
            process_status.process_type = enum.ProcessType.NOTIFICATIONS.value
        if status == 0:
            process_status.start_process_date = datetime.utcnow()
            process_status.status = "process started"
            process_status.percent = 0
        elif status == 1:
            process_status.status = "process run"
            process_status.percent = percent
        else:
            process_status.status = "process finished"
            process_status.percent = 100
        process_status.all_items = all_items
        process_status.updated_items = updated_items
        process_status.update_status()
        return "successfully update process status"
    except Exception as e:
        print('problem with update process status. ', e)
        return "failed to update process status"


def tickers_notifications(user):
    try:
        candidates = retrieve_user_candidates(user)
        tickers_arr = [x['ticker'] for x in candidates]
        delim = ","
        data = api_service.current_stock_price(delim.join(tickers_arr))

        prices = json.loads(data)
        notifications_data = [
            {'ticker': x['ticker'], 'buying_target_price_fmp': x['buying_target_price_fmp'], 'price': y['price'], 'stocke_score': x['algotrader_rank'], 'underpriced': x['under_priced_pnt'], 'beta': x['beta'], 'website': x['website'], 'company': x['company_name'], 'taret': 0 if x['target_mean_price'] is None else x['target_mean_price'], 'taret_pt': 0 if x['target_mean_price'] is None else ((x['target_mean_price'] - y['price']) * 100)/y['price']}
            for x in
            candidates for y in prices if
            x['ticker'] == y['symbol'] and x['buying_target_price_fmp'] >= y['price']]

        notifications_today = Notification.query.filter(Notification.email == user,
                                                        Notification.date >= datetime.utcnow().date()).all()
        tickers_sends = [x.ticker for x in notifications_today]
        notifications_data = [x for x in notifications_data if x['ticker'] not in tickers_sends]
        tickers_names = [x['ticker'] for x in notifications_data]
        if len(notifications_data) > 0:
            send_email(recipient=user,
                       subject=f'BUY signal from Stock Score: {delim.join(tickers_names)}',
                       template='account/email/tickers_notification',
                       data=notifications_data,
                       user=user)
            for n in notifications_data:
                notification = Notification(
                    email=user,
                    date=datetime.utcnow().date(),
                    ticker=n['ticker']
                )
                db.session.add(notification)
                db.session.commit()
        return {"status": 0, "error": ""}
    except Exception as e:
        print('problem with notifications', e)
        return {"status": 2, "error": e}
    # return f"tickers count: {len(notifications_data)} \n {json.dumps(notifications_data)}"


def save_process_data(data):
    now = datetime.utcnow()
    try:
        last_update_data = NotificationProcess.query.order_by(NotificationProcess.start_process_time.desc()).first()
        update_data = NotificationProcess()
        if data['error_status'] == '1':
            update_data.error_status = True
            update_data.last_update_date = last_update_data.last_update_date if last_update_data is not None else now
        else:
            update_data.last_update_date = data['end_time']
            update_data.error_status = False
        update_data.start_process_time = data['start_time']
        update_data.end_process_time = data['end_time']
        update_data.avg_time_by_user = data['avg_update_times']
        update_data.num_of_users = data['num_of_users']
        update_data.num_users_received = data['num_users_received']
        update_data.update_data()
        return "successfully update date"
    except Exception as e:
        print('problem with update last date. ', e)
        return "failed to update date"
