import json
import math

from flask import (
    Blueprint,
    request
)
from datetime import datetime
from app import csrf
from app.models import TickerData, LastUpdateSpyderData
from app.research.fmp_research import get_fmp_ratings_score_for_ticker
from app.research.stock_invest_research import get_stock_invest_rank_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_finance_research import get_yahoo_rank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker, get_info_for_ticker

test = Blueprint('test', __name__)

@csrf.exempt
@test.route('/updatemarketdataforcandidate_test', methods=['POST'])
def updatemarketdataforcandidate_test():
    ticker = request.form['ticker_to_update']
    try:
        result = research_ticker(ticker)
        return result
    except Exception as e:
        print('problem with research', e)
        return json.dumps({"status": 2, "error": e})


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
    error_status = 1 if len(sections) > 0 else 0
    print('ended')
    print(datetime.now())
    return json.dumps({"status": error_status, "sections": sections})


@csrf.exempt
@test.route('/savelasttimeforupdatedata_test', methods=['POST'])
def savelasttimeforupdatedata_test():
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
        # update_data.update_data()
        return "successfully update date"
    except Exception as e:
        print('problem with update last date. ', e)
        return "failed to update date"