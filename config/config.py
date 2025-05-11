# config/configpi.py

import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

openai.api_key = os.getenv("OPENAI_API_KEY")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "stephen.novaassist.ai@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")