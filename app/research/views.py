import json
import math

from flask import (
    Blueprint,
    request, url_for
)
from datetime import datetime

from werkzeug.utils import redirect

from app import csrf
from app.email import send_email
from app.models import TickerData, Candidate, LastUpdateSpyderData, ReportStatistic, Report
from app.research.fmp_research import get_fmp_ratings_score_for_ticker
from app.research.stock_invest_research import get_stock_invest_rank_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_finance_research import get_yahoo_rank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker, get_info_for_ticker

research = Blueprint('research', __name__)


@csrf.exempt
@research.route('/updatemarketdataforcandidate', methods=['POST'])
def updatemarketdataforcandidate():
    ticker = request.form['ticker_to_update']
    try:
        m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
        result = research_ticker(ticker)
    except Exception as e:
        print('problem with research', e)
    finally:
        return redirect(url_for('admin.market_data'))

@csrf.exempt
@research.route('/updatemarketdataforcandidatespider', methods=['POST'])
def updatemarketdataforcandidatespider():
    ticker = request.form['ticker_to_update']
    try:
        m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
        updated = m_data.updated_server_time.date()
        today = datetime.now().date()

        if updated != today:
            result = research_ticker(ticker)
            return result
        else:
            return json.dumps({"status": 0, "sections": []})
        # result, log = research_ticker(ticker)
        # return result, log
    except Exception as e:
        print('problem with research', e)
        return json.dumps({"status": 2, "error": e})

@csrf.exempt
@research.route('/savelasttimeforupdatedata', methods=['POST'])
def savelasttimeforupdatedata():
    error_status = request.form['error_status']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    num_of_positions = request.form['num_of_positions']
    error_tickers = request.form['error_tickers']
    research_error_tickers = request.form['research_error_tickers']
    updated_tickers = request.form['updated_tickers']
    already_updated_tickers = request.form['already_updated_tickers']
    avg_update_times = request.form['avg_update_times']
    error_tickers_num = request.form['error_tickers_num']

    now = datetime.utcnow()
    try:
        last_update_data = LastUpdateSpyderData.query.order_by(LastUpdateSpyderData.start_process_time.desc()).first()
        update_data = LastUpdateSpyderData()
        if error_status == '1':
            update_data.error_status = True
            update_data.error_tickers = error_tickers
            update_data.last_update_date = last_update_data.last_update_date if last_update_data is not None else now
        else:
            update_data.last_update_date = end_time
            update_data.error_status = False
            update_data.error_tickers = '[]'
        update_data.start_process_time = start_time
        update_data.end_process_time = end_time
        update_data.avg_time_by_position = avg_update_times
        update_data.num_of_positions = num_of_positions
        update_data.research_error_tickers = research_error_tickers
        update_data.already_updated_tickers = already_updated_tickers
        update_data.updated_tickers = updated_tickers
        update_data.error_tickers_num = error_tickers_num
        update_data.update_data()
        return "successfully update date"
    except Exception as e:
        print('problem with update last date. ', e)
        return "failed to update date"


@csrf.exempt
@research.route('/update_reports_statistic', methods=['GET'])
def update_reports_statistic():
    try:
        reports = Report.query.all()
        for r in reports:
            snapshot = ReportStatistic()
            snapshot.email = r.email
            snapshot.report_time = r.report_time
            snapshot.net_liquidation = r.net_liquidation
            snapshot.remaining_sma_with_safety = r.remaining_sma_with_safety
            snapshot.remaining_trades = r.remaining_trades
            snapshot.all_positions_value = r.all_positions_value
            snapshot.open_positions_json = r.open_positions_json
            snapshot.open_orders_json = r.open_orders_json
            snapshot.dailyPnl = r.dailyPnl
            snapshot.last_worker_execution = r.last_worker_execution
            snapshot.market_time = r.market_time
            snapshot.market_state = r.market_state
            snapshot.excess_liquidity = r.excess_liquidity
            snapshot.candidates_live_json = r.candidates_live_json
            snapshot.started_time = r.started_time
            snapshot.api_connected = r.api_connected
            snapshot.market_data_error = r.market_data_error
            snapshot.add_report()
        return "successfully update reports statistic"
    except:
        print('problem with update reports statistic')
        return "update reports statistic failed"


def research_ticker(ticker):
    print('started')
    print(datetime.now())
    marketdata = TickerData()
    marketdata.ticker = ticker
    sections = []
    try:
        marketdata.tipranks, marketdata.twelve_month_momentum = get_tiprank_for_ticker(ticker)
    except:
        sections.append("tiprank")
        print("ERROR in MarketDataResearch for "+ticker+". Section: tiprank")

    # try:
    #     marketdata.stock_invest_rank = get_stock_invest_rank_for_ticker(ticker)
    # except:
    #     sections.append("stockinvest")
    #     print("ERROR in MarketDataResearch for "+ticker+" section: stockinvest")

    try:
        marketdata.yahoo_rank, marketdata.under_priced_pnt,marketdata.target_mean_price = get_yahoo_rank_for_ticker(ticker)
    except:
        sections.append("yahooRank")
        print("ERROR in MarketDataResearch for "+ticker+" section: yahooRank")

    try:
        marketdata.fmp_rating, marketdata.fmp_score = get_fmp_ratings_score_for_ticker(ticker)
    except:
        sections.append("fmpRating")
        print("ERROR in MarketDataResearch for "+ticker+" section: fmpRating")

    try:
        marketdata.yahoo_avdropP, marketdata.yahoo_avspreadP, marketdata.max_intraday_drop_percent = get_yahoo_stats_for_ticker(ticker)
    except:
        sections.append("yahooStats")
        print("ERROR in MarketDataResearch for "+ticker+" section: yahooStats")

    try:
        info = get_info_for_ticker(ticker)
        marketdata.beta = info['beta']
    except:
        sections.append("Beta yahooStats")
        print("ERROR in Info research for "+ticker+" section: yahooStats")

    if len(sections) > 0:
        send_email(recipient='support@algotrader.company',
                   subject='Algotrader research problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker,
                   sections=", ".join(sections))

    #defaults for exceptions
    if math.isnan(marketdata.yahoo_avdropP):
        marketdata.yahoo_avdropP = 0
    if math.isnan(marketdata.yahoo_avspreadP):
        marketdata.yahoo_avspreadP = 0
    if math.isnan(marketdata.target_mean_price):
        marketdata.target_mean_price = 0
    if marketdata.beta is None:
        marketdata.beta = 0
    ct = datetime.utcnow()

    marketdata.updated_server_time = ct
    marketdata.algotrader_rank = 0 if marketdata.tipranks == 0 \
                                      or marketdata.yahoo_rank is None \
                                      or marketdata.yahoo_rank == 6 \
                                   else marketdata.tipranks/2 + 6 - marketdata.yahoo_rank

    marketdata.add_ticker_data()
    error_status = 1 if len(sections) > 0 else 0
    print('ended')
    print(datetime.now())
    return json.dumps({"status": error_status, "sections": sections})


@csrf.exempt
@research.route('/alltickers', methods=['GET'])  # for use from the task
def alltickers():
    cands = Candidate.query.filter_by(enabled=True).group_by(Candidate.ticker).all()
    resp = []
    for c in cands:
        resp.append(c.ticker)
    return json.dumps(resp)



