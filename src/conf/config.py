import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET = 1234567890
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_SECONDS = 3600


config = Config()
