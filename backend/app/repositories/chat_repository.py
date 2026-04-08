from datetime import datetime, timezone
from typing import Any

from app.config.database import db


class ChatRepository:
    def __init__(self) -> None:
        self.sessions = db["chat_sessions"]
        self.messages = db["chat_messages"]

    async def find_active_session(self, user_id: str) -> dict[str, Any] | None:
        return await self.sessions.find_one(
            {"user_id": user_id, "active": True},
            sort=[("created_at", -1)],
        )

    async def create_session(
        self,
        session_id: str,
        user_id: str,
        greeting: str = "",
    ) -> dict[str, Any]:
        doc = {
            "session_id": session_id,
            "user_id": user_id,
            "active": True,
            "created_at": datetime.now(timezone.utc),
            "greeting": greeting,
        }
        await self.sessions.insert_one(doc)
        return doc

    async def deactivate_sessions(self, user_id: str) -> None:
        await self.sessions.update_many(
            {"user_id": user_id, "active": True},
            {"$set": {"active": False}},
        )

    async def save_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        text: str,
    ) -> None:
        await self.messages.insert_one(
            {
                "session_id": session_id,
                "user_id": user_id,
                "role": role,
                "text": text,
                "created_at": datetime.now(timezone.utc),
            }
        )

    async def get_messages(
        self,
        session_id: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        cursor = (
            self.messages.find(
                {"session_id": session_id},
                {"_id": 0, "role": 1, "text": 1, "created_at": 1},
            )
            .sort("created_at", 1)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)
