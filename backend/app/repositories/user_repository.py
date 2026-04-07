from bson import ObjectId
from bson.errors import InvalidId

from app.config.database import db


class UserRepository:
    """Data access layer for user documents in MongoDB."""

    def __init__(self) -> None:
        """Initialize repository with users collection reference."""
        self.collection = db["users"]

    async def create(self, user_data: dict[str, object]) -> dict[str, object]:
        """Create a new user document.

        Args:
            user_data: User document to insert.

        Returns:
            The inserted user data with string ID.
        """
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    async def find_by_email(self, email: str) -> dict[str, object] | None:
        """Find user by email address.

        Args:
            email: Email to search for.

        Returns:
            User document if found, None otherwise.
        """
        user = await self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def find_by_id(self, user_id: str) -> dict[str, object] | None:
        """Find user by ID.

        Args:
            user_id: User ID string to search for.

        Returns:
            User document if found, None otherwise.
        """
        try:
            oid = ObjectId(user_id)
        except (InvalidId, TypeError):
            return None

        user = await self.collection.find_one({"_id": oid})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def find_by_national_id(self, national_id: str) -> dict[str, object] | None:
        """Find user by national ID (DNI/NIE).

        Args:
            national_id: National ID to search for.

        Returns:
            User document if found, None otherwise.
        """
        user = await self.collection.find_one({"national_id": national_id})
        if user:
            user["_id"] = str(user["_id"])
        return user
