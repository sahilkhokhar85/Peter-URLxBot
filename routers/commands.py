import html

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, LinkPreviewOptions, Message

from config import Settings
from services.caption_style_store import CaptionStyleStore
from services.format_preference_store import FormatPreferenceStore
from services.thumbnail_store import ThumbnailStore
from utils import text
from utils.callbacks import CaptionStyleCallback, FormatCallback, SettingsCallback
from utils.keyboards import (
    about_keyboard,
    caption_style_keyboard,
    format_preference_keyboard,
    help_keyboard,
    settings_keyboard,
    start_keyboard,
)

router = Router(name="commands")

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
CAPTION_ORDER = ["normal", "bold", "italic", "mono"]


def _mention(user) -> str:
    name = html.escape(user.first_name or "there") if user else "there"
    uid = user.id if user else 0
    return f'<a href="tg://user?id={uid}">{name}</a>'


async def _send_start(target: Message, user, settings: Settings) -> None:
    caption = text.START_TEXT.format(mention=_mention(user))
    if settings.start_image_url:
        try:
            await target.answer_photo(
                settings.start_image_url,
                caption=caption,
                reply_markup=start_keyboard(),
            )
            return
        except TelegramAPIError:
            pass
    await target.answer(
        caption,
        reply_markup=start_keyboard(),
        link_preview_options=NO_PREVIEW,
    )


def _is_authorized(message: Message, settings: Settings) -> bool:
    return bool(message.from_user) and message.from_user.id in settings.auth_users


async def _settings_markup(
    user_id: int,
    thumbnail_store: ThumbnailStore,
    format_store: FormatPreferenceStore,
    caption_store: CaptionStyleStore,
):
    return settings_keyboard(
        thumbnail_store.get(user_id) is not None,
        await caption_store.get(user_id),
        await format_store.get(user_id),
    )


@router.message(Command("start"), F.chat.type == "private")
async def start_command(message: Message, settings: Settings) -> None:
    if not _is_authorized(message, settings):
        await message.answer("🚫 You're not authorized to use this bot.")
        return
    await _send_start(message, message.from_user, settings)


@router.message(Command("help"), F.chat.type == "private")
async def help_command(message: Message, settings: Settings) -> None:
    if not _is_authorized(message, settings):
        await message.answer("🚫 You're not authorized to use this bot.")
        return
    await message.answer(
        text.HELP_TEXT,
        reply_markup=help_keyboard(),
        link_preview_options=NO_PREVIEW,
    )


@router.message(Command("about"), F.chat.type == "private")
async def about_command(message: Message, settings: Settings) -> None:
    if not _is_authorized(message, settings):
        await message.answer("🚫 You're not authorized to use this bot.")
        return
    await message.answer(
        text.ABOUT_TEXT,
        reply_markup=about_keyboard(),
        link_preview_options=NO_PREVIEW,
    )


@router.message(Command("settings"), F.chat.type == "private")
async def settings_command(
    message: Message,
    settings: Settings,
    thumbnail_store: ThumbnailStore,
    format_store: FormatPreferenceStore,
    caption_store: CaptionStyleStore,
) -> None:
    if not _is_authorized(message, settings):
        await message.answer("🚫 You're not authorized to use this bot.")
        return
    markup = await _settings_markup(
        message.from_user.id, thumbnail_store, format_store, caption_store
    )
    await message.answer(text.SETTINGS_TEXT, reply_markup=markup)


@router.message(Command("setformat"), F.chat.type == "private")
async def setformat_command(
    message: Message, settings: Settings, format_store: FormatPreferenceStore
) -> None:
    if not _is_authorized(message, settings):
        await message.answer("🚫 You're not authorized to use this bot.")
        return
    current = await format_store.get(message.from_user.id)
    await message.answer(
        "Choose your default send format for direct links:",
        reply_markup=format_preference_keyboard(current),
    )


@router.callback_query(FormatCallback.filter())
async def format_callback(
    query: CallbackQuery, callback_data: FormatCallback, format_store: FormatPreferenceStore
) -> None:
    if not query.message or not query.from_user:
        await query.answer()
        return
    if callback_data.value == "ask":
        await format_store.clear(query.from_user.id)
    else:
        await format_store.set(query.from_user.id, callback_data.value)
    await query.message.edit_reply_markup(
        reply_markup=format_preference_keyboard(callback_data.value)
    )
    await query.answer("Saved!")


@router.message(Command("setcaption", "set_caption"), F.chat.type == "private")
async def setcaption_command(
    message: Message, settings: Settings, caption_store: CaptionStyleStore
) -> None:
    if not _is_authorized(message, settings):
        await message.answer("🚫 You're not authorized to use this bot.")
        return
    current = await caption_store.get(message.from_user.id)
    await message.answer(
        "Choose your caption style:",
        reply_markup=caption_style_keyboard(current),
    )


@router.callback_query(CaptionStyleCallback.filter())
async def caption_style_callback(
    query: CallbackQuery, callback_data: CaptionStyleCallback, caption_store: CaptionStyleStore
) -> None:
    if not query.message or not query.from_user:
        await query.answer()
        return
    await caption_store.set(query.from_user.id, callback_data.value)
    await query.message.edit_reply_markup(
        reply_markup=caption_style_keyboard(callback_data.value)
    )
    await query.answer("Saved!")


@router.callback_query(SettingsCallback.filter())
async def settings_callback(
    query: CallbackQuery,
    callback_data: SettingsCallback,
    thumbnail_store: ThumbnailStore,
    format_store: FormatPreferenceStore,
    caption_store: CaptionStyleStore,
) -> None:
    message = query.message
    if not message or not query.from_user:
        await query.answer()
        return

    user_id = query.from_user.id
    action = callback_data.action

    if action == "thumb":
        if thumbnail_store.get(user_id):
            await query.answer(
                "Thumbnail is set. Send a new photo to replace it.", show_alert=True
            )
        else:
            await query.answer(
                "Send me a photo to set your thumbnail.", show_alert=True
            )
        return

    if action == "delthumb":
        if not thumbnail_store.delete(user_id):
            await query.answer("No thumbnail to delete.", show_alert=True)
            return
    elif action == "caption":
        current = await caption_store.get(user_id) or "normal"
        if current in CAPTION_ORDER:
            nxt = CAPTION_ORDER[(CAPTION_ORDER.index(current) + 1) % len(CAPTION_ORDER)]
        else:
            nxt = "normal"
        await caption_store.set(user_id, nxt)
    elif action == "format":
        current = await format_store.get(user_id)
        if current == "media":
            await format_store.set(user_id, "document")
        elif current == "document":
            await format_store.clear(user_id)
        else:
            await format_store.set(user_id, "media")

    markup = await _settings_markup(
        user_id, thumbnail_store, format_store, caption_store
    )

    if action == "open" and getattr(message, "photo", None):
        # The start screen is a photo message. Replace it with a buttons-only screen.
        await message.answer(text.SETTINGS_TEXT, reply_markup=markup)
        await message.delete()
    elif action == "open":
        await message.edit_text(text.SETTINGS_TEXT, reply_markup=markup)
    else:
        await message.edit_reply_markup(reply_markup=markup)

    await query.answer()


async def _show(message, body: str, keyboard) -> None:
    if getattr(message, "photo", None):
        await message.edit_caption(caption=body, reply_markup=keyboard)
    else:
        await message.edit_text(
            body,
            reply_markup=keyboard,
            link_preview_options=NO_PREVIEW,
        )


async def handle_ui_callback(
    callback: CallbackQuery, action: str, settings: Settings
) -> None:
    message = callback.message
    if not message:
        await callback.answer()
        return

    if action == "home":
        if getattr(message, "photo", None) or not settings.start_image_url:
            await _show(
                message,
                text.START_TEXT.format(mention=_mention(callback.from_user)),
                start_keyboard(),
            )
        else:
            # Coming back from a text screen (Settings): bring the start image back.
            await _send_start(message, callback.from_user, settings)
            await message.delete()
    elif action == "help":
        await _show(message, text.HELP_TEXT, help_keyboard())
    elif action == "about":
        await _show(message, text.ABOUT_TEXT, about_keyboard())
    elif action == "close":
        await message.delete()

    await callback.answer()
