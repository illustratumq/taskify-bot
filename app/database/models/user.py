import sqlalchemy as sa

from app.database.models.base import TimedBaseModel


class User(TimedBaseModel):
    user_id = sa.Column(sa.BIGINT(), primary_key=True, autoincrement=False, index=True)
    full_name = sa.Column(sa.VARCHAR(255), nullable=False)
    mention = sa.Column(sa.VARCHAR(300), nullable=False)
    phone_number = sa.Column(sa.VARCHAR(12), nullable=True)
    notify = sa.Column(sa.BOOLEAN(), nullable=False, default=True)
