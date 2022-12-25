from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from src import db


class LoginAttempt(db.Model):
    __tablename__ = "login_attempt"
    login_attempt_id: int = db.Column(Integer, primary_key=True)
    email: str = db.Column(String(128))
    password_hash: str = db.Column(String(256))
    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
