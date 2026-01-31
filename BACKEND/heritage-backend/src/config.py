from pathlib import Path
import os

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Change this to a secure key in production
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'  # Enable debug mode based on environment variable