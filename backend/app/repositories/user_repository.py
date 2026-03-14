from typing import Any

from bson import ObjectId

from app.config.database import db


class UserRepository:
    def __init__(self) -> None:
        self.collection = db["users"]

    async def create(self, user_data: dict[str, Any]) -> dict[str, Any]:
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        user = await self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def find_by_national_id(self, national_id: str) -> dict[str, Any] | None:
        user = await self.collection.find_one({"national_id": national_id})
        if user:
            user["_id"] = str(user["_id"])
        return user
