import json

import chromadb
from . import chunker as ch
import ollama

chromaClient = chromadb.Client()
# noinspection PyTypeChecker
collStocks = chromaClient.create_collection(
    'stocks'
    , configuration={
        "hnsw": {"space": "cosine"}
    }
)

def saveStockDataInDB(scriptSymbol, stockData):
    print("Creating Chunks for ", scriptSymbol)
    chunks = ch.chunkStockData(scriptSymbol, stockData)
    print("Created Chunks for ", scriptSymbol)
    print("Creating Embeddings for ", scriptSymbol)
    embeddings = getEmbeddings(chunks)
    print("Created Embeddings for ", scriptSymbol)
    print("Saving Chunks for ", scriptSymbol)
    writeDB(chunks, embeddings)
    print("Saved Chunks for ", scriptSymbol)


def getEmbeddings(chunks):
    print("Retrieving Embeddings for ", len(chunks))
    response = ollama.embed(
        model="nomic-embed-text",
        input=[chunk['text'] for chunk in chunks]
    )
    print("Retrieved Embeddings for ", len(chunks))
    # print(response)
    return response['embeddings']


def writeDB(chunks, embeddings):
    for chunk, embedding in zip(chunks, embeddings):
        collStocks.add(
            ids=chunk['id'],
            embeddings=embedding,
            metadatas=chunk['metadata'],
            documents=chunk['text']
        )


def queryDB(question, nResults=5):
    vector = ollama.embed(
        model="nomic-embed-text",
        input=[question]
    )
    print("Retrieved Embeddings for Q ", question)
    results = collStocks.query(
        query_embeddings=[vector['embeddings'][0]],
        n_results=nResults,
        include=['documents', 'metadatas', 'distances']
    )
    return results


if __name__ == "__main__":
    import sys

    sys.path.append('..')
    from app.fetcher import getStockData
    symbol = "RELIANCE.NS"
    print("Fetching Data from Source for ", symbol)
    data = getStockData(symbol)
    print("Received Data from Source for ", symbol)
    saveStockDataInDB(symbol, data)
    print("Retrieved Count for VectorDB: ", collStocks.count())

    results = queryDB("What is Reliance's revenue trend?")
    # print(json.dumps(results, indent=2))
    # for i, doc in enumerate(results['documents'][0]):
    #     print(results['metadatas'][0][i], "| distance:", results['distances'][0][i])
    #     print(doc[:100])
    #     print("--"*100)
    print(getAnswer(results, True))
