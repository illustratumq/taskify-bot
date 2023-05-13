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
