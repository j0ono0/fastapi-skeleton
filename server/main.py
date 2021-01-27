
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from starlette.staticfiles import StaticFiles
from sql_app.database import engine
from server import authentication as auth
from .routers import user
from sql_app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#Middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)

# Routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user.router)
app.include_router(auth.router)


##########################################
# Routers

@app.get("/")
def homepage():
    return {
        'homepage': True,
        'fastapi': 'Working OK. Try user: pass below...',
        'admin@johnnewall.com': 'admin'
    }
