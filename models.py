from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# ---- USER MODEL ----
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'


# ---- JOB MODEL ----
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.String(50), default='Full-Time')
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Job {self.title}>'


# ---- INTERNSHIP MODEL ----
class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    stipend = db.Column(db.String(50), default='Unpaid')
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Internship {self.title}>'


# ---- ALUMNI MODEL ----
class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    current_job = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    linkedin = db.Column(db.String(200))
    bio = db.Column(db.Text)
    photo = db.Column(db.String(200))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Alumni {self.name}>'