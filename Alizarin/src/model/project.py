from datetime import datetime
from sqlalchemy import DateTime

from src import db
from .project_users import project_users

class Project(db.Model):
    __tablename__: str = "projects"
    project_id = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128))
    users = db.relationship('User', secondary='project_users', back_populates='projects')
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    created_by = db.relationship('User')

    sprints = db.relationship("Sprint", back_populates="project")
    stories = db.relationship("Story", back_populates="project")

    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, name: str, created_by: object):
        self.name = name
        self.created_by = created_by
