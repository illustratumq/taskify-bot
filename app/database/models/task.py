import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from app.database.models.base import TimedBaseModel
from app.database.services.enums import TaskStatusEnum
from app.misc.times import localize, now


class Task(TimedBaseModel):
    task_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    subject_id = sa.Column(sa.BIGINT, sa.ForeignKey('subjects.subject_id', ondelete='SET NULL'), nullable=False)
    name = sa.Column(sa.VARCHAR(255), nullable=False)
    description = sa.Column(sa.VARCHAR(1500), nullable=True)
    grade = sa.Column(sa.INTEGER, nullable=True)
    deadline = sa.Column(sa.DateTime, nullable=True)
    status = sa.Column(ENUM(TaskStatusEnum), default=TaskStatusEnum.ACTIVE, nullable=False)

    def task_status_text(self):
        return {
            TaskStatusEnum.ACTIVE: '🟠 Не виконано',
            TaskStatusEnum.COMPLETE: '🟢 Виконано',
            TaskStatusEnum.WASTED: '🔴 Тобі пезда блять'
        }.get(self.status)

    async def is_deadline_wasted(self, task_db):
        check = localize(self.deadline) < now()
        if check:
            await task_db.update_task(self.task_id, status=TaskStatusEnum.WASTED)
        return check
