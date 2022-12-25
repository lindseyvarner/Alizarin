from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from src import db
from .sprint import Sprint
from .project import Project

class Task(db.Model):
    task_id: int = db.Column(Integer, primary_key=True)
    name: str = db.Column(String(128))
    description: str = db.Column(String(512))
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.sprint_id"))
    sprint = db.relationship("Sprint", back_populates="tasks")
    is_completed: bool = db.Column(db.Boolean())
    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)
    __tablename__ = "tasks"

    def __init__(self, name, description, sprint: Sprint):
        self.name = name
        self.description = description
        self.sprint = sprint
        self.is_completed = False
