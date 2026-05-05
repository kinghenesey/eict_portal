import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'eict-secret-key-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///eict_portal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'emmanuelkingchris@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'ohde ikyl nbcn xame')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', 'emmanuelkingchris@gmail.com')