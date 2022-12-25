from datetime import datetime
from sqlalchemy import DateTime

from src import db
from .project_users import project_users

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name: str = db.Column(db.String(128))
    last_name: str = db.Column(db.String(128))
    email: str = db.Column(db.String(128))
    password_hash: str = db.Column(db.String(256))
    projects = db.relationship('Project', secondary='project_users', back_populates='users')

    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, first_name, last_name, email, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
