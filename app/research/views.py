import json
import math

from flask import (
    Blueprint,
    redirect,
    request,
    url_for
)
from datetime import datetime
from app import csrf
from app.email import send_email
from app.models import TickerData, Candidate, LastUpdateSpyderData, ReportStatistic, Report
from app.research.fmp_research import get_fmp_ratings_score_for_ticker
from app.research.stock_invest_research import get_stock_invest_rank_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_finance_research import get_yahoo_rank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker, get_beta_for_ticker

research = Blueprint('research', __name__)


@csrf.exempt
@research.route('/updatemarketdataforcandidate', methods=['POST'])
def updatemarketdataforcandidate():
    ticker = request.form['ticker_to_update']
    try:
        m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
        updated=m_data.updated_server_time.date()
        today = datetime.now().date()
        if updated!=today:
            research_ticker(ticker)
    except:
        print('problem with research')
    return redirect(url_for('admin.market_data'))


@csrf.exempt
@research.route('/savelasttimeforupdatedata', methods=['POST'])
def savelasttimeforupdatedata():
    error_status = request.form['error_status']
    error_message = request.form['error_message']
    now = datetime.utcnow()
    try:
        last_update_data = LastUpdateSpyderData.query.first()
        if last_update_data is None:
            last_update_data = LastUpdateSpyderData()
        last_update_data.process_date_time = now
        if error_status == '1':
            last_update_data.error_status = True
            last_update_data.error_message = error_message
        else:
            last_update_data.last_update_date = now
            last_update_data.error_status = False
            last_update_data.error_message = ''
        last_update_data.update_data()
        return "successfully update date"
    except:
        print('problem with update last date')
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
    marketdata = TickerData()
    marketdata.ticker = ticker
    try:
        marketdata.tipranks, marketdata.twelve_month_momentum = get_tiprank_for_ticker(ticker)
    except:
        print("ERROR in MarketDataResearch for "+ticker+" section: tiprank")
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Tipranks problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.stock_invest_rank = get_stock_invest_rank_for_ticker(ticker)
    except:
        print("ERROR in MarketDataResearch for "+ticker+" section: stockinvest")
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Stock Invest problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.yahoo_rank, marketdata.under_priced_pnt,marketdata.target_mean_price = get_yahoo_rank_for_ticker(ticker)
    except:
        print("ERROR in MarketDataResearch for "+ticker+" section: yahooRank")
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Yahoo Rank problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.fmp_rating, marketdata.fmp_score = get_fmp_ratings_score_for_ticker(ticker)
    except:
        print("ERROR in MarketDataResearch for "+ticker+" section: fmpRating")
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research FMP Score problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.yahoo_avdropP, marketdata.yahoo_avspreadP,marketdata.beta = get_yahoo_stats_for_ticker(ticker)
    except:
        print("ERROR in MarketDataResearch for "+ticker+" section: yahooStats")
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Yahoo Stats problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.beta = get_beta_for_ticker(ticker)
    except:
        print("ERROR in Beta research for "+ticker+" section: yahooStats")
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Beta problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    #defaults for exceptions
    if math.isnan(marketdata.yahoo_avdropP):
        marketdata.yahoo_avdropP = 0
    if math.isnan(marketdata.yahoo_avspreadP):
        marketdata.yahoo_avspreadP = 0
    if math.isnan(marketdata.target_mean_price):
        marketdata.target_mean_price = 0
    if math.isnan(marketdata.beta):
        marketdata.beta = 0
    ct = datetime.utcnow()

    marketdata.updated_server_time = ct
    marketdata.add_ticker_data()


@csrf.exempt
@research.route('/alltickers', methods=['GET'])  # for use from the task
def alltickers():
    cands = Candidate.query.filter_by(enabled=True).group_by(Candidate.ticker).all()
    resp = []
    for c in cands:
        resp.append(c.ticker)
    return json.dumps(resp)
