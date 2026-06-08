from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.db.session import Base, engine
from app.routes.events import router as events_router
from app.routes.cop import router as cop_router
from app.routes.analyst import router as analyst_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SitRep Fusion API",
    description="Railway-ready TRL 4 prototype for multidomain sensing, fusion, COP, and decision support.",
    version="0.1.0",
)

app.include_router(events_router)
app.include_router(cop_router)
app.include_router(analyst_router)

dashboard_dir = Path(__file__).resolve().parents[1] / "dashboard"

if dashboard_dir.exists():
    app.mount("/static", StaticFiles(directory=str(dashboard_dir)), name="static")

@app.get("/")
def root():
    return {
        "service": "SitRep Fusion API",
        "status": "online",
        "docs": "/docs",
        "dashboard": "/dashboard",
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    index_file = dashboard_dir / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<h1>SitRep Fusion API online</h1><p>Dashboard folder not found, but API is running.</p>"
