from flask_app.run import app
from dotenv import load_dotenv
import os

SECRET_KEY = '11223344'
DEBUG = True
PORT = 5000

app.config['WTF_CSRF_ENABLED'] = False

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
