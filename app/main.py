from fastapi import FastAPI
from pydantic import BaseModel
from .fetcher import getStockData
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates")

class StockSymbol(BaseModel):
    symbol: str
    query: str
    debugMode: bool


app = FastAPI()
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/fetch")
async def fetch(request: StockSymbol):
    return getStockData(request.symbol)



