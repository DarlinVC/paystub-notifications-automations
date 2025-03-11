from fastapi import FastAPI
from app.controllers import paystub_controller
app = FastAPI()

app.include_router(paystub_controller.router)
