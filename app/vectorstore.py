import chromadb

chromaClient = chromadb.Client()
collStocks = chromaClient.create_collection(
    'stocks'
    , configuration={
        "hnsw": {"space": "cosine"}
    }
)
print(collStocks.name)