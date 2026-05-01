from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from datetime import datetime

app = FastAPI()

# Evita bloqueos de seguridad cuando Netlify pida los datos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/noticias")
def obtener_noticias():
    # Podés cambiar los tickers por los que RYE siga más de cerca
    tickers = ["GGAL", "YPF", "SPY", "AL30.BA"]
    noticias = []

    for ticker in tickers:
        tk = yf.Ticker(ticker)
        for news in tk.news[:2]:  
            try:
                fecha_pub = datetime.fromtimestamp(news.get("providerPublishTime")).strftime('%d/%m/%Y')
            except:
                fecha_pub = "Reciente"

            noticias.append({
                "ticker": ticker,
                "titulo": news.get("title"),
                "link": news.get("link"),
                "fecha": fecha_pub,
                "fuente": news.get("publisher", "Mercado")
            })

    return noticias