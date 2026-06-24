import yfinance

def getStockData(symbol):
    stock = yfinance.Ticker(symbol)
    return buildStockData(stock)

def buildStockData(stock):
    summary = stock.info.get('longBusinessSummary')
    currentPrice = stock.info.get('currentPrice')
    trailingPE = stock.info.get('trailingPE')
    fiftyTwoWeekHigh = stock.info.get('fiftyTwoWeekHigh')
    fiftyTwoWeekLow = stock.info.get('fiftyTwoWeekLow')
    marketCap = stock.info.get('marketCap')
    news = getStockNews(stock)
    recommendations = stock.recommendations.to_string()
    financials = stock.financials.to_string()
    return {
        'summary': summary,
        'currentPrice': currentPrice,
        'trailingPE': trailingPE,
        'fiftyTwoWeekHigh': fiftyTwoWeekHigh,
        'fiftyTwoWeekLow': fiftyTwoWeekLow,
        'marketCap': marketCap,
        'news': news,
        'recommendations': recommendations,
        'financials': financials
    }

def getStockNews(stock):
    news = stock.news
    returnValue = []
    for article in news:
        returnValue.append(article['content']['summary'])
    return returnValue




