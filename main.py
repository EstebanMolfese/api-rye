from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser
import html
import time
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/noticias")
def obtener_noticias():
    # Usamos una búsqueda de economía y mercados para Argentina
    rss_url = "https://news.google.com/rss/search?q=economía+mercado+argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    
    try:
        feed = feedparser.parse(rss_url)
        
        # Si por alguna razón está vacío, probamos con la sección de negocios general
        if not feed.entries:
            fallback_url = "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=es-419&gl=AR&ceid=AR:es-419"
            feed = feedparser.parse(fallback_url)

        noticias = []
        for entry in feed.entries[:10]:
            try:
                # Separamos el título de la fuente (Google News los une con un guion)
                partes = entry.title.rsplit(' - ', 1)
                titulo_limpio = partes[0]
                fuente_media = partes[1] if len(partes) > 1 else "Economía"
                
                # Formateo de fecha seguro
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    fecha_pub = time.strftime('%d/%m/%Y', entry.published_parsed)
                else:
                    fecha_pub = "Reciente"

                noticias.append({
                    "ticker": "ECONOMÍA",
                    "titulo": html.unescape(titulo_limpio),
                    "link": entry.link,
                    "fecha": fecha_pub,
                    "fuente": fuente_media
                })
            except:
                continue 
                
        return noticias
    except Exception as e:
        print(f"Error en el radar: {e}")
        return []
