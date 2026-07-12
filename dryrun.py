from app.fetcher import getStockData
from app.vectorstore import saveStockDataInDB, collStocks
from app.rag import getAnswer

symbol = "RELIANCE.NS"

print("Fetching data...")
data = getStockData(symbol)

print("Saving to DB...")
saveStockDataInDB(symbol, data)
print("Count:", collStocks.count())

print("Asking question...")
# result = getAnswer("What is Reliance's revenue trend?", debugMode=True)
result = getAnswer("Is Reliance a good buy based on its financials ?", debugMode=True)
print("Answer:", result['answer'])
print("Debug chunks:")
for chunk in result['debugChunks']:
    print(chunk['type'], "| distance:", chunk['distance'])
    print(chunk['text'][:1000])
    print("---")