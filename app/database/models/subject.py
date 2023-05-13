import sqlalchemy as sa

from app.database.models.base import TimedBaseModel


class Subject(TimedBaseModel):
    subject_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = sa.Column(sa.BIGINT, sa.ForeignKey('users.user_id', ondelete='SET NULL'), nullable=False)
    name = sa.Column(sa.VARCHAR(255), nullable=False)
    description = sa.Column(sa.VARCHAR(500), nullable=False)
    grade = sa.Column(sa.INTEGER, nullable=False)
    tag = sa.Column(sa.VARCHAR(100), nullable=False)
