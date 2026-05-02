from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser
import html
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
    # Esta URL está filtrada específicamente por el tema "Economía, Negocios y Mercados"
    # hl=es-419 (Idioma), gl=AR (Región Argentina), ceid=AR:es-419 (ID de búsqueda)
    rss_url = "https://news.google.com/rss/topics/CAAqBwgKMMq_0Asw-o6pAw?hl=es-419&gl=AR&ceid=AR:es-419"
    
    try:
        feed = feedparser.parse(rss_url)
        noticias = []
        
        # Tomamos las 10 noticias más recientes del mercado
        for entry in feed.entries[:10]:
            # Limpiamos el título para separar la noticia del diario (ej: "Sube el Dólar - Ámbito")
            partes = entry.title.rsplit(' - ', 1)
            titulo_limpio = partes[0]
            fuente_media = partes[1] if len(partes) > 1 else "Mercado"
            
            noticias.append({
                "ticker": "ECONOMÍA",
                "titulo": html.unescape(titulo_limpio),
                "link": entry.link,
                "fecha": datetime(*entry.published_parsed[:6]).strftime('%d/%m/%Y'),
                "fuente": fuente_media
            })
            
        return noticias
    except Exception as e:
        print(f"Error en el radar: {e}")
        return []
