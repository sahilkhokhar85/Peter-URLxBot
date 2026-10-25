from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import Settings
from services.user_store import UserStore
from utils.runtime import format_uptime, uptime_seconds

router = Router(name="admin")
logger = logging.getLogger(__name__)

OWNER_ONLY = "🚫 This command is for the owner only."


def _is_owner(message: Message, settings: Settings) -> bool:
    return bool(message.from_user) and message.from_user.id == settings.owner_id


def _parse_user_id(raw: str | None) -> int | None:
    if not raw:
        return None
    try:
        return int(raw.split()[0])
    except ValueError:
        return None


@router.message(Command("ban"), F.chat.type == "private")
async def ban_command(
    message: Message,
    command: CommandObject,
    settings: Settings,
    user_store: UserStore,
) -> None:
    if not _is_owner(message, settings):
        await message.answer(OWNER_ONLY)
        return

    target = _parse_user_id(command.args)
    if target is None:
        await message.answer("Usage: <code>/ban user_id</code>")
        return
    if target == settings.owner_id:
        await message.answer("You cannot ban the owner.")
        return

    await user_store.set_banned(target, True)
    logger.info("User banned | owner=%s target=%s", message.from_user.id, target)
    await message.answer(f"🚫 User <code>{target}</code> is banned.")


@router.message(Command("unban"), F.chat.type == "private")
async def unban_command(
    message: Message,
    command: CommandObject,
    settings: Settings,
    user_store: UserStore,
) -> None:
    if not _is_owner(message, settings):
        await message.answer(OWNER_ONLY)
        return

    target = _parse_user_id(command.args)
    if target is None:
        await message.answer("Usage: <code>/unban user_id</code>")
        return

    await user_store.set_banned(target, False)
    logger.info("User unbanned | owner=%s target=%s", message.from_user.id, target)
    await message.answer(f"✅ User <code>{target}</code> is unbanned.")


@router.message(Command("stats"), F.chat.type == "private")
async def stats_command(
    message: Message,
    settings: Settings,
    user_store: UserStore,
) -> None:
    if not _is_owner(message, settings):
        await message.answer(OWNER_ONLY)
        return

    stats = await user_store.stats()
    await message.answer(
        "<b>📊 Bot stats!!</b>\n\n"
        "<blockquote>"
        f"<b>🔥 Active users:</b> {stats['active']} in last 24 hrs\n"
        f"<b>👥 Total users:</b> {stats['total']}\n"
        f"<b>🚫 Banned users:</b> {stats['banned']}\n\n"
        f"<b>⏱ Uptime:</b> {format_uptime(uptime_seconds())}"
        "</blockquote>"
    )
