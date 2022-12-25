from src import db

project_users = db.Table(
    "project_users",
    db.Column("project_id", db.ForeignKey("projects.project_id"), primary_key=True),
    db.Column("user_id", db.ForeignKey("users.user_id"), primary_key=True),
)
