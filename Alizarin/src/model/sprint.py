from datetime import datetime
from src import db
from .project import Project
from sqlalchemy import DateTime

class Sprint(db.Model):
    __tablename__ = "sprints"
    sprint_id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="sprints")
    tasks = db.relationship("Task", back_populates="sprint")
    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, name: str, project: Project):
        self.name = name
        self.project_id = project
