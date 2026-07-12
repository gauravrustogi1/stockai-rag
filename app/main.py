from fastapi import FastAPI
from pydantic import BaseModel
from .fetcher import getStockData
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .vectorstore import saveStockDataInDB
from .rag import getAnswer

templates = Jinja2Templates(directory="app/templates")

class StockSymbol(BaseModel):
    sym1: str
    sym2: str
    sym3: str

class AskRequest(BaseModel):
    question: str
    debugMode: bool

app = FastAPI()
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/load")
async def loadStockData(symbols: StockSymbol):
    try:
        if len(symbols.sym1.strip())>0:
            stockData1 = getStockData(symbols.sym1)
            saveStockDataInDB(symbols.sym1, stockData1)
        if len(symbols.sym2.strip())>0:
            stockData2 = getStockData(symbols.sym2)
            saveStockDataInDB(symbols.sym2, stockData2)
        if len(symbols.sym3.strip())>0:
            stockData3 = getStockData(symbols.sym3)
            saveStockDataInDB(symbols.sym3, stockData3)
    except Exception as e:
        return {"error": str(e)}
    return {"success": True}

@app.post("/ask")
async def askStockData(request: AskRequest):
    return getAnswer(request.question, request.debugMode)


# async def fetch(request: StockSymbol):
#     return getStockData(request.symbol)



