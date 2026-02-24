from fastapi import FastAPI
from app.routes import chatbot

app = FastAPI()

app.include_router(chatbot.router)
