from functools import lru_cache
from fastapi import Depends, FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from starlette.staticfiles import StaticFiles
from server.user.routes import user_router, groups_router
from server.metadata import tags
from database import engine
engine.Base.metadata.create_all(bind=engine.engine)

# Load and cache env settings
from . import config
@lru_cache()
def get_settings():
    return config.Settings()

settings = get_settings()

app = FastAPI()
#Middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)

# Routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router)
app.include_router(groups_router)


##########################################
# Routers

@app.get("/")
def homepage(settings: config.Settings = Depends(get_settings)):
    return {
        'homepage': True,
        'fastapi': 'Working OK. Try user: pass below...',
        'admin@johnnewall.com': 'admin'
    }
