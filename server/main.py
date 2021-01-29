
from fastapi import Depends, FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from starlette.staticfiles import StaticFiles
from server.user.routes import user_router, groups_router
from server.metadata import tags
from database.db_config import Base, engine

from . import server_config


Base.metadata.create_all(bind=engine)

settings = server_config.get_settings()

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
def homepage(settings: server_config.Settings = Depends(server_config.get_settings)):
    return {
        'homepage': True,
        'fastapi': 'Working OK. Try user: pass below...',
        'admin@johnnewall.com': 'admin'
    }
