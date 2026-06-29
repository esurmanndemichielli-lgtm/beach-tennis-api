from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import videos, matches, players

app = FastAPI(
    title="Beach Tennis Scout API",
    description="API para analise automatica de partidas de Beach Tennis com IA",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(matches.router, prefix="/api/matches", tags=["matches"])
app.include_router(players.router, prefix="/api/players", tags=["players"])

@app.get("/")
def root():
    return {"status": "ok", "message": "API do Beach Tennis Scout rodando!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
