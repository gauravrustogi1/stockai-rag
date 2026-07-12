from collections import defaultdict

def chunkStockData(symbol, stockData):
    summaryChunk = createSummaryChunk(symbol, stockData)
    metricsChunk = createMetricsChunk(symbol, stockData)
    newsChunk = createNewsChunk(symbol, stockData)
    recommendationsChunk = createRecommendationsChunk(symbol, stockData)
    financialsChunk = createFinancialsChunk(symbol, stockData)
    returnValue = []
    returnValue.append(summaryChunk)
    returnValue.append(metricsChunk)
    for news in newsChunk if len(newsChunk) > 0 else []:
        returnValue.append(news)
    for recommendations in recommendationsChunk if len(recommendationsChunk) > 0 else []:
        returnValue.append(recommendations)
    for financials in financialsChunk if len(financialsChunk) > 0 else []:
        returnValue.append(financials)

    return returnValue


def createFinancialsChunk(symbol, stockData):
    financialsChunk = []
    keywords = {
        "revenue": ["revenue", "gross profit"]
        , "ebitda": ["ebitda", "operating income"]
        , "netincome": ["net income", "tax"]
        , "expenses": ["expenses", "cost"]
    }

    intermediateVar = defaultdict(list)
    for rowLabel, row in stockData['financials'].iterrows():
        matched = False
        for kwKey, matches in keywords.items():
            for match in matches:
                if rowLabel.lower().find(match) != -1:
                    matched = True
                    intermediateVar[kwKey].append(f"{rowLabel} | " + " | ".join([f"{str(col)[:10]}: {formatIndianNumber(val)}" for col, val in row.items() if str(val) != 'nan']))
        if not matched:
            intermediateVar['other_financial_data'].append(
                f"{rowLabel} | " + " | ".join([
                    f"{str(col)[:10]}: {formatIndianNumber(val)}"
                    for col, val in row.items()
                    if str(val) != 'nan'
                ])
            )

    for k, v in intermediateVar.items():
        financialsChunk.append({
            'id': f"{symbol}_financials_{k}"
            , 'metadata': {'symbol': symbol, 'type':f"financials_{k}"}
            , 'text': "\n".join(v)
        })

    return financialsChunk


def createRecommendationsChunk(symbol, stockData):
    recommendationsChunk = []
    # i = 0
    for index, row in stockData['recommendations'].iterrows():
        chunk = {}
        chunk.update({'id': f"{symbol}_recommendation_{index}"})
        chunk.update({'metadata': {'symbol': symbol, 'type':'recommendation', 'period': row['period']}})
        chunk.update({'text': f"{row['period']}"
                      f" | Strong Buy: {row['strongBuy']}"
                      f" | Buy: {row['buy']}"
                      f" | Hold: {row['hold']}"
                      f" | Sell: {row['sell']}"
                      f" | Strong Sell: {row['strongSell']}"
                      })
        recommendationsChunk.append(chunk)
    return recommendationsChunk



def createNewsChunk(symbol, stockData):
    newsChunk = []
    i = 0
    for news in stockData['news']:
        chunk = {}
        chunk.update({'id': f"{symbol}_news_{i}"})
        chunk.update({'metadata': {'symbol': symbol, 'type':'news'}})
        chunk.update({'text': news})
        newsChunk.append(chunk)
        i += 1
    return newsChunk



def createMetricsChunk(symbol, stockData):
    metricsChunk = {}
    metricsChunk.update({'id':f"{symbol}_metrics"})
    metricsChunk.update({'metadata': {'symbol':symbol, 'type':'metrics'}})
    metricsChunk.update({
        'text': f"Stock Metrics and Current Price Data:"
                f" Current Price: {stockData['currentPrice']}"
                f" | PE Ratio: {stockData['trailingPE']}"
                f" | 52W High: {stockData['fiftyTwoWeekHigh']}"
                f" | 52W Low: {stockData['fiftyTwoWeekLow']}"
                f" | Market Cap: {formatIndianNumber(stockData['marketCap'])}"
    })
    return metricsChunk


def createSummaryChunk(symbol, stockData):
    summaryChunk = {}
    summaryChunk.update({'id': f"{symbol}_summary"})
    summaryChunk.update({'metadata': {'symbol': symbol, 'type': 'summary'}})
    summaryChunk.update({'text': stockData['summary']})
    return summaryChunk

def formatIndianNumber(val):
    crores = val / 10_000_000
    return f"₹{crores:,.2f} Cr"

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from app.fetcher import getStockData
    data = getStockData("RELIANCE.NS")
    chunks = chunkStockData("RELIANCE.NS", data)
