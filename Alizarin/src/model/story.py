from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from src import db


class Story(db.Model):
    __tablename__ = "stories"
    story_id: int = db.Column(db.Integer, primary_key=True)
    content: str = db.Column(db.String(2048))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="stories")

    created_at: datetime = db.Column(DateTime, default=datetime.utcnow)

    def __int__(self, content, project):
        self.content = content
        self.project = project
