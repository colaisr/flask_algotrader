from . import TickerData, Fgi_score
from .. import db
from ..api_service.api_service import fundamentals_summary_api


class TelegramSignal(db.Model):
    __tablename__ = 'TelegramSignals'
    id = db.Column('id', db.Integer, primary_key=True)
    ticker = db.Column('ticker', db.String)
    transmitted = db.Column('transmitted', db.Boolean)
    received = db.Column('received', db.DateTime)
    signal_price = db.Column('signal_price', db.Float)
    target_price = db.Column('target_price', db.Float)
    profit_percent = db.Column('profit_percent', db.Float)
    target_met = db.Column('target_met', db.DateTime)
    days_to_get = db.Column('days_to_get', db.Integer)

    buy_algotrader_rank = db.Column('buy_algotrader_rank', db.Float)
    buy_beta = db.Column('buy_beta', db.Float)
    buy_max_intraday_drop_percent = db.Column('buy_max_intraday_drop_percent', db.Float)
    buy_average_drop_percent = db.Column('buy_average_drop_percent', db.Float)
    buy_average_spread_percent = db.Column('buy_average_spread_percent', db.Float)
    buy_yahoo_rank = db.Column('buy_yahoo_rank', db.Float)
    buy_tipranks = db.Column('buy_tipranks', db.Integer)
    buy_underpriced_percent = db.Column('buy_underpriced_percent', db.Float)
    buy_12m_momentum = db.Column('buy_12m_momentum', db.Float)
    buy_target_low_yahoo = db.Column('buy_target_low_yahoo', db.Float)
    buy_target_medium_yahoo = db.Column('buy_target_medium_yahoo', db.Float)
    buy_target_high_yahoo = db.Column('buy_target_high_yahoo', db.Float)
    buy_tr_hedgeFundTrendValue = db.Column('buy_tr_hedgeFundTrendValue', db.Float)
    buy_tr_bloggerSectorAvg = db.Column('buy_tr_bloggerSectorAvg', db.Float)
    buy_tr_bloggerBullishSentiment = db.Column('buy_tr_bloggerBullishSentiment', db.Float)
    buy_tr_insidersLast3MonthsSum = db.Column('buy_tr_insidersLast3MonthsSum', db.Float)
    buy_tr_newsSentimentsBearishPercent = db.Column('buy_tr_newsSentimentsBearishPercent', db.Float)
    buy_tr_newsSentimentsBullishPercent = db.Column('buy_tr_newsSentimentsBullishPercent', db.Float)
    buy_tr_priceTarget = db.Column('buy_tr_priceTarget', db.Float)
    buy_tr_fundamentalsReturnOnEquity = db.Column('buy_tr_fundamentalsReturnOnEquity', db.Float)
    buy_tr_fundamentalsAssetGrowth = db.Column('buy_tr_fundamentalsAssetGrowth', db.Float)
    buy_tr_sma = db.Column('buy_tr_sma', db.String)
    buy_tr_analystConsensus = db.Column('buy_tr_analystConsensus', db.String)
    buy_tr_hedgeFundTrend = db.Column('buy_tr_hedgeFundTrend', db.String)
    buy_tr_insiderTrend = db.Column('buy_tr_insiderTrend', db.String)
    buy_tr_newsSentiment = db.Column('buy_tr_newsSentiment', db.String)
    buy_tr_bloggerConsensus = db.Column('buy_tr_bloggerConsensus', db.String)

    buy_fgi = db.Column('buy_fgi', db.Integer)

    buy_dividendYieldTTM = db.Column('buy_dividendYieldTTM', db.Float)
    buy_payoutRatioTTM = db.Column('buy_payoutRatioTTM', db.Float)
    buy_cashRatioTTM = db.Column('buy_cashRatioTTM', db.Float)
    buy_daysOfPayablesOutstandingTTM = db.Column('buy_daysOfPayablesOutstandingTTM', db.Float)
    buy_grossProfitMarginTTM = db.Column('buy_grossProfitMarginTTM', db.Float)
    buy_netProfitMarginTTM = db.Column('buy_netProfitMarginTTM', db.Float)
    buy_returnOnEquityTTM = db.Column('buy_returnOnEquityTTM', db.Float)
    buy_debtRatioTTM = db.Column('buy_debtRatioTTM', db.Float)
    buy_totalDebtToCapitalizationTTM = db.Column('buy_totalDebtToCapitalizationTTM', db.Float)
    buy_receivablesTurnoverTTM = db.Column('buy_receivablesTurnoverTTM', db.Float)
    buy_fixedAssetTurnoverTTM = db.Column('buy_fixedAssetTurnoverTTM', db.Float)
    buy_freeCashFlowOperatingCashFlowRatioTTM = db.Column('buy_freeCashFlowOperatingCashFlowRatioTTM', db.Float)
    buy_priceToFreeCashFlowsRatioTTM = db.Column('buy_priceToFreeCashFlowsRatioTTM', db.Float)
    buy_peRatioTTM = db.Column('buy_peRatioTTM', db.Float)
    buy_currentRatioTTM = db.Column('buy_currentRatioTTM', db.Float)
    buy_daysOfSalesOutstandingTTM = db.Column('buy_daysOfSalesOutstandingTTM', db.Float)
    buy_operatingCycleTTM = db.Column('buy_operatingCycleTTM', db.Float)
    buy_operatingProfitMarginTTM = db.Column('buy_operatingProfitMarginTTM', db.Float)
    buy_effectiveTaxRateTTM = db.Column('buy_effectiveTaxRateTTM', db.Float)
    buy_returnOnCapitalEmployedTTM = db.Column('buy_returnOnCapitalEmployedTTM', db.Float)
    buy_debtEquityRatioTTM = db.Column('buy_debtEquityRatioTTM', db.Float)
    buy_cashFlowToDebtRatioTTM = db.Column('buy_cashFlowToDebtRatioTTM', db.Float)
    buy_payablesTurnoverTTM = db.Column('buy_payablesTurnoverTTM', db.Float)
    buy_freeCashFlowPerShareTTM = db.Column('buy_freeCashFlowPerShareTTM', db.Float)
    buy_priceToBookRatioTTM = db.Column('buy_priceToBookRatioTTM', db.Float)
    buy_priceEarningsToGrowthRatioTTM = db.Column('buy_priceEarningsToGrowthRatioTTM', db.Float)
    buy_quickRatioTTM = db.Column('buy_quickRatioTTM', db.Float)
    buy_daysOfInventoryOutstandingTTM = db.Column('buy_daysOfInventoryOutstandingTTM', db.Float)
    buy_cashConversionCycleTTM = db.Column('buy_cashConversionCycleTTM', db.Float)
    buy_pretaxProfitMarginTTM = db.Column('buy_pretaxProfitMarginTTM', db.Float)
    buy_returnOnAssetsTTM = db.Column('buy_returnOnAssetsTTM', db.Float)
    buy_netIncomePerEBTTTM = db.Column('buy_netIncomePerEBTTTM', db.Float)
    buy_longTermDebtToCapitalizationTTM = db.Column('buy_longTermDebtToCapitalizationTTM', db.Float)
    buy_companyEquityMultiplierTTM = db.Column('buy_companyEquityMultiplierTTM', db.Float)
    buy_inventoryTurnoverTTM = db.Column('buy_inventoryTurnoverTTM', db.Float)
    buy_cashPerShareTTM = db.Column('buy_cashPerShareTTM', db.Float)
    buy_priceToSalesRatioTTM = db.Column('buy_priceToSalesRatioTTM', db.Float)
    buy_dividendPerShareTTM = db.Column('buy_dividendPerShareTTM', db.Float)

    def add_signal(self):
        signal = TelegramSignal.query.filter((TelegramSignal.ticker == self.ticker) & (TelegramSignal.received == self.received)).first()
        if signal is None:
            self.add_market_info()
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def update_signal(self):
        db.session.commit()

    def add_market_info(self):
        last_market_data = TickerData.query.filter_by(ticker=self.ticker).order_by(TickerData.updated_server_time.desc()).first()
        self.buy_algotrader_rank = last_market_data.algotrader_rank
        self.buy_beta = last_market_data.beta
        self.buy_max_intraday_drop_percent = last_market_data.max_intraday_drop_percent
        self.buy_average_drop_percent = last_market_data.yahoo_avdropP
        self.buy_average_spread_percent = last_market_data.yahoo_avspreadP
        self.buy_yahoo_rank = last_market_data.yahoo_rank
        self.buy_tipranks = last_market_data.tipranks
        self.buy_underpriced_percent = last_market_data.under_priced_pnt
        self.buy_12m_momentum = last_market_data.twelve_month_momentum
        self.buy_target_low_yahoo = last_market_data.target_low_price_yahoo
        self.buy_target_medium_yahoo = last_market_data.target_mean_price
        self.buy_target_high_yahoo = last_market_data.target_high_price_yahoo
        self.buy_tr_hedgeFundTrendValue = last_market_data.tr_hedgeFundTrendValue
        self.buy_tr_bloggerSectorAvg = last_market_data.tr_bloggerSectorAvg
        self.buy_tr_bloggerBullishSentiment = last_market_data.tr_bloggerBullishSentiment
        self.buy_tr_insidersLast3MonthsSum = last_market_data.tr_insidersLast3MonthsSum
        self.buy_tr_newsSentimentsBearishPercent = last_market_data.tr_newsSentimentsBearishPercent
        self.buy_tr_newsSentimentsBullishPercent = last_market_data.tr_newsSentimentsBullishPercent
        self.buy_tr_priceTarget = last_market_data.tr_priceTarget
        self.buy_tr_fundamentalsReturnOnEquity = last_market_data.tr_fundamentalsReturnOnEquity
        self.buy_tr_fundamentalsAssetGrowth = last_market_data.tr_fundamentalsAssetGrowth
        self.buy_tr_sma = last_market_data.tr_sma
        self.buy_tr_analystConsensus =last_market_data.tr_analystConsensus
        self.buy_tr_hedgeFundTrend = last_market_data.tr_hedgeFundTrend
        self.buy_tr_insiderTrend = last_market_data.tr_insiderTrend
        self.buy_tr_newsSentiment = last_market_data.tr_newsSentiment
        self.buy_tr_bloggerConsensus = last_market_data.tr_bloggerConsensus

        market_emotion = Fgi_score.query.order_by(Fgi_score.score_time.desc()).first()
        self.buy_fgi=market_emotion.fgi_value
        fundamentals=fundamentals_summary_api(self.ticker)[0]

        self.buy_dividendYieldTTM = fundamentals['dividendYieldTTM']
        self.buy_payoutRatioTTM = fundamentals['payoutRatioTTM']
        self.buy_cashRatioTTM = fundamentals['cashRatioTTM']
        self.buy_daysOfPayablesOutstandingTTM = fundamentals['daysOfPayablesOutstandingTTM']
        self.buy_grossProfitMarginTTM = fundamentals['grossProfitMarginTTM']
        self.buy_netProfitMarginTTM = fundamentals['netProfitMarginTTM']
        self.buy_returnOnEquityTTM = fundamentals['returnOnEquityTTM']
        self.buy_debtRatioTTM = fundamentals['debtRatioTTM']
        self.buy_totalDebtToCapitalizationTTM = fundamentals['totalDebtToCapitalizationTTM']
        self.buy_receivablesTurnoverTTM = fundamentals['receivablesTurnoverTTM']
        self.buy_fixedAssetTurnoverTTM = fundamentals['fixedAssetTurnoverTTM']
        self.buy_freeCashFlowOperatingCashFlowRatioTTM = fundamentals['freeCashFlowOperatingCashFlowRatioTTM']
        self.buy_priceToFreeCashFlowsRatioTTM = fundamentals['priceToFreeCashFlowsRatioTTM']
        self.buy_peRatioTTM = fundamentals['peRatioTTM']
        self.buy_currentRatioTTM = fundamentals['currentRatioTTM']
        self.buy_daysOfSalesOutstandingTTM = fundamentals['daysOfSalesOutstandingTTM']
        self.buy_operatingCycleTTM = fundamentals['operatingCycleTTM']
        self.buy_operatingProfitMarginTTM = fundamentals['operatingProfitMarginTTM']
        self.buy_effectiveTaxRateTTM = fundamentals['effectiveTaxRateTTM']
        self.buy_returnOnCapitalEmployedTTM = fundamentals['returnOnCapitalEmployedTTM']
        self.buy_debtEquityRatioTTM = fundamentals['debtEquityRatioTTM']
        self.buy_cashFlowToDebtRatioTTM = fundamentals['cashFlowToDebtRatioTTM']
        self.buy_payablesTurnoverTTM = fundamentals['payablesTurnoverTTM']
        self.buy_freeCashFlowPerShareTTM = fundamentals['freeCashFlowPerShareTTM']
        self.buy_priceToBookRatioTTM = fundamentals['priceToBookRatioTTM']
        self.buy_priceEarningsToGrowthRatioTTM = fundamentals['priceEarningsToGrowthRatioTTM']
        self.buy_quickRatioTTM = fundamentals['quickRatioTTM']
        self.buy_daysOfInventoryOutstandingTTM = fundamentals['daysOfInventoryOutstandingTTM']
        self.buy_cashConversionCycleTTM = fundamentals['cashConversionCycleTTM']
        self.buy_pretaxProfitMarginTTM = fundamentals['pretaxProfitMarginTTM']
        self.buy_returnOnAssetsTTM = fundamentals['returnOnAssetsTTM']
        self.buy_netIncomePerEBTTTM = fundamentals['netIncomePerEBTTTM']
        self.buy_longTermDebtToCapitalizationTTM = fundamentals['longTermDebtToCapitalizationTTM']
        self.buy_companyEquityMultiplierTTM = fundamentals['companyEquityMultiplierTTM']
        self.buy_inventoryTurnoverTTM = fundamentals['inventoryTurnoverTTM']
        self.buy_cashPerShareTTM = fundamentals['cashPerShareTTM']
        self.buy_priceToSalesRatioTTM = fundamentals['priceToSalesRatioTTM']
        self.buy_dividendPerShareTTM = fundamentals['dividendPerShareTTM']

