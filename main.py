from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from datetime import datetime
import requests

app = FastAPI()

# 1. Configuración de CORS para que tu sitio en Netlify pueda leer los datos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Configuración de Sesión para evitar bloqueos de Yahoo Finance
# Esto añade un "User-Agent" que simula un navegador Chrome real
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

@app.get("/noticias")
def obtener_noticias():
    # Tickers de interés para RyE Consultora
    tickers = ["GGAL", "YPF", "SPY", "AL30.BA"]
    noticias = []
    
    for ticker in tickers:
        try:
            # Iniciamos el ticker usando la sesión segura
            tk = yf.Ticker(ticker, session=session)
            items_news = tk.news
            
            if not items_news:
                continue

            # Procesamos las últimas 2 noticias de cada activo
            for news in items_news[:2]:
                # Extracción robusta de campos (verifica minúsculas y mayúsculas)
                titulo = news.get("title") or news.get("Title") or f"Actualidad de {ticker}"
                link = news.get("link") or news.get("Link") or "#"
                fuente = news.get("publisher") or news.get("Publisher") or "Mercado"
                
                # Gestión de fecha con validación de timestamp
                timestamp = news.get("providerPublishTime") or news.get("ProviderPublishTime")
                if timestamp:
                    try:
                        fecha_pub = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
                    except:
                        fecha_pub = "Reciente"
                else:
                    fecha_pub = "Reciente"

                noticias.append({
                    "ticker": ticker,
                    "titulo": titulo,
                    "link": link,
                    "fecha": fecha_pub,
                    "fuente": fuente
                })
        except Exception as e:
            # Si un ticker falla, continuamos con el siguiente para no romper la API
            print(f"Error procesando {ticker}: {e}")
            continue
            
    return noticias