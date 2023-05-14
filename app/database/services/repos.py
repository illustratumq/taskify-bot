from app.database.models import *
from app.database.services.db_ctx import BaseRepo


class UserRepo(BaseRepo[User]):
    model = User

    async def get_user(self, user_id: int) -> User:
        return await self.get_one(self.model.user_id == user_id)

    async def update_user(self, user_id: int, **kwargs) -> None:
        return await self.update(self.model.user_id == user_id, **kwargs)

    async def delete_user(self, user_id: int):
        return await self.delete(self.model.user_id == user_id)


class TaskRepo(BaseRepo[Task]):
    model = Task

    async def get_task(self, task_id: int) -> Task:
        return await self.get_one(self.model.task_id == task_id)

    async def get_task_subject(self, subject_id: int) -> list[Task]:
        return await self.get_all(self.model.subject_id == subject_id)

    async def update_task(self, task_id: int, **kwargs) -> None:
        return await self.update(self.model.task_id == task_id, **kwargs)

    async def delete_task(self, task_id: int):
        return await self.delete(self.model.task_id == task_id)


class SubjectRepo(BaseRepo[Subject]):
    model = Subject
    async def get_subject(self, subject_id: int) -> Subject:
        return await self.get_one(self.model.subject_id == subject_id)

    async def get_subject_user(self, user_id: int) -> list[Subject]:
        return await self.get_all(self.model.user_id == user_id)

    async def get_tag_user(self, user_id: int, tag: int) -> list[Subject]:
        return await self.get_all(self.model.tag == tag, self.model.user_id == user_id)

    async def update_subject(self, subject_id: int, **kwargs) -> None:
        return await self.update(self.model.subject_id == subject_id, **kwargs)

    async def delete_subject(self, subject_id: int):
        return await self.delete(self.model.subject_id == subject_id)