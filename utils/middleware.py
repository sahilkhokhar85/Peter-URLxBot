from __future__ import annotations

import logging

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from services.user_store import UserStore

logger = logging.getLogger(__name__)


class UserTrackerMiddleware(BaseMiddleware):
    """Records every user who talks to the bot and blocks banned users."""

    def __init__(self, user_store: UserStore, owner_id: int) -> None:
        self.user_store = user_store
        self.owner_id = owner_id

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)

        if user is not None and not user.is_bot:
            try:
                if user.id != self.owner_id and await self.user_store.is_banned(user.id):
                    if isinstance(event, Message):
                        await event.answer("🚫 You are banned from using this bot.")
                    elif isinstance(event, CallbackQuery):
                        await event.answer(
                            "🚫 You are banned from using this bot.", show_alert=True
                        )
                    return None
                await self.user_store.touch(user.id)
            except Exception:  # pylint: disable=broad-except
                logger.exception("User tracking failed | user=%s", user.id)

        return await handler(event, data)
