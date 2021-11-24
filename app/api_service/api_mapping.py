def financial_ttm_mapping(obj):
    property_list = []
    p = {"priority": 1, "field_name": "Dividend Yield", "value": obj["dividendYielPercentageTTM"], "tooltip": 5}
    property_list.append(p)
    p = {"priority": 2, "field_name": "P/E", "value": obj["peRatioTTM"], "tooltip": 4}
    property_list.append(p)
    p = {"priority": 3, "field_name": "PEG", "value": obj["pegRatioTTM"], "tooltip": 6}
    property_list.append(p)
    p = {"priority": 4, "field_name": "Payout Ratio", "value": obj["payoutRatioTTM"], "tooltip": 7}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Current Ratio", "value": obj["currentRatioTTM"], "tooltip": 8}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Quick Ratio", "value": obj["quickRatioTTM"], "tooltip": 9}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Cash Ratio ", "value": obj["cashRatioTTM"], "tooltip": 53}
    property_list.append(p)
    p = {"priority": 1, "field_name": "DSO", "value": obj["daysOfSalesOutstandingTTM"], "tooltip": 10}
    property_list.append(p)
    p = {"priority": 1, "field_name": "DSI", "value": obj["daysOfInventoryOutstandingTTM"], "tooltip": 11}
    property_list.append(p)
    p = {"priority": 1, "field_name": "DPO", "value": obj["daysOfPayablesOutstandingTTM"], "tooltip": 12}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Operating Cycle", "value": obj["operatingCycleTTM"], "tooltip": 22}
    property_list.append(p)
    p = {"priority": 1, "field_name": "CCC", "value": obj["cashConversionCycleTTM"], "tooltip": 13}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Gross Profit Margin", "value": obj["grossProfitMarginTTM"], "tooltip": 14}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Operating Profit Margin", "value": obj["operatingProfitMarginTTM"], "tooltip": 15}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Pretax Profit Margin", "value": obj["pretaxProfitMarginTTM"], "tooltip": 16}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Net Profit Margin", "value": obj["netProfitMarginTTM"], "tooltip": 17}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Tax Rate", "value": obj["effectiveTaxRateTTM"], "tooltip": 18}
    property_list.append(p)
    p = {"priority": 1, "field_name": "ROA", "value": obj["returnOnAssetsTTM"], "tooltip": 19}
    property_list.append(p)
    p = {"priority": 1, "field_name": "ROE", "value": obj["returnOnEquityTTM"], "tooltip": 20}
    property_list.append(p)
    p = {"priority": 1, "field_name": "ROCE", "value": obj["returnOnCapitalEmployedTTM"], "tooltip": 21}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Net Income Per EBT", "value": obj["netIncomePerEBTTTM"], "tooltip": 23}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Debt  ratio", "value": obj["debtRatioTTM"], "tooltip": 24}
    property_list.append(p)
    p = {"priority": 1, "field_name": "D/E", "value": obj["debtEquityRatioTTM"], "tooltip": 25}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Long-term Debt to Cap", "value": obj["longTermDebtToCapitalizationTTM"], "tooltip": 26}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Total Debt to Capitalization", "value": obj["totalDebtToCapitalizationTTM"], "tooltip": 27}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Cash Flow to Debt", "value": obj["cashFlowToDebtRatioTTM"], "tooltip": 29}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Equity Multiplier", "value": obj["companyEquityMultiplierTTM"], "tooltip": 30}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Receivables Turnover", "value": obj["receivablesTurnoverTTM"], "tooltip": 31}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Payables Turnover ", "value": obj["payablesTurnoverTTM"], "tooltip": 32}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Inventory Turnover ", "value": obj["inventoryTurnoverTTM"], "tooltip": 33}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Fixed Assets Turnover ", "value": obj["fixedAssetTurnoverTTM"], "tooltip": 34}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Free Cash Flow per Share", "value": obj["freeCashFlowPerShareTTM"], "tooltip": 36}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Cash Per Share", "value": obj["cashPerShareTTM"], "tooltip": 37}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Free Cash Flow to Operating Cash Flow Ratio ", "value": obj["freeCashFlowOperatingCashFlowRatioTTM"], "tooltip": 38}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Price-To-Book", "value": obj["priceToBookRatioTTM"], "tooltip": 39}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Price-to-Sales", "value": obj["priceToSalesRatioTTM"], "tooltip": 40}
    property_list.append(p)
    p = {"priority": 1, "field_name": "Price to Free Cash Flow", "value": obj["priceToFreeCashFlowsRatioTTM"], "tooltip": 41}
    property_list.append(p)
    p = {"priority": 1, "field_name": "P/CF", "value": obj["priceCashFlowRatioTTM"], "tooltip": 42}
    property_list.append(p)
    p = {"priority": 1, "field_name": "DPS", "value": obj["dividendPerShareTTM"], "tooltip": 43}
    property_list.append(p)



    return property_list