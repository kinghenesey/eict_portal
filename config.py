import os

class Config:
    SECRET_KEY = 'eict-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///eict_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'emmanuelkingchris@gmail.com'      # ← put your Gmail here
    MAIL_PASSWORD = 'ohde ikyl nbcn xame'     # ← we'll set this up below
    MAIL_DEFAULT_SENDER = 'emmanuelkingchris@gmail.com' # ← same Gmail