import sqlalchemy as sa

from app.database.models.base import TimedBaseModel


class Task(TimedBaseModel):
    task_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    subject_id = sa.Column(sa.BIGINT, sa.ForeignKey('subjects.subject_id', ondelete='SET NULL'), nullable=False)
    name = sa.Column(sa.VARCHAR(255), nullable=False)
    description = sa.Column(sa.VARCHAR(1500), nullable=True)
    grade = sa.Column(sa.INTEGER, nullable=True)
    deadline = sa.Column(sa.DateTime, nullable=True)
