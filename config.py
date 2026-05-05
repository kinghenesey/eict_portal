import os

class Config:
    SECRET_KEY = 'eict-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///eict_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False