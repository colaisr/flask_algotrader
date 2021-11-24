def financial_ttm_mapping(obj):
    property_list = []
    p = {"priority": 1, "field_name": "Dividend Yield  ", "value": obj["dividendYielPercentageTTM"], "tooltip": 1}
    property_list.append(p)
    p = {"priority": 2, "field_name": "P/E", "value": obj["peRatioTTM"], "tooltip": 1}
    property_list.append(p)
    p = {"priority": 3, "field_name": "PEG", "value": obj["pegRatioTTM"], "tooltip": 1}
    property_list.append(p)
    p = {"priority": 4, "field_name": "Payout Ratio", "value": obj["payoutRatioTTM"], "tooltip": 1}
    property_list.append(p)

    return property_list