
from fastapi import FastAPI

from app.routers import scrapping_router
from app.routers.user_router import router as user_router
from app.routers.scrapping_router import router as scrapping_router
from app.routers.scrapping_router_enhanced import  router as scrapping_router_enhanced
app = FastAPI()
@app.get("/")
def greet():
    return "Hello World"

app.include_router(user_router)
app.include_router(scrapping_router)
app.include_router(scrapping_router_enhanced)


