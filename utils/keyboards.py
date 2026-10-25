from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbacks import RequestCallback, UiCallback
from utils.models import DownloadOption
from utils.callbacks import FormatCallback
from utils.callbacks import CaptionStyleCallback
from utils.callbacks import SettingsCallback


def start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Help", callback_data=UiCallback(action="help").pack()
        ),
        InlineKeyboardButton(
            text="Settings", callback_data=SettingsCallback(action="open").pack()
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="About", callback_data=UiCallback(action="about").pack()
        )
    )
    return builder.as_markup()


def help_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Settings", callback_data=SettingsCallback(action="open").pack()
        ),
        InlineKeyboardButton(
            text="About", callback_data=UiCallback(action="about").pack()
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Home", callback_data=UiCallback(action="home").pack()
        )
    )
    return builder.as_markup()


def about_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Home", callback_data=UiCallback(action="home").pack()
        ),
        InlineKeyboardButton(
            text="Help", callback_data=UiCallback(action="help").pack()
        ),
    )
    return builder.as_markup()


CAPTION_LABELS = {
    "normal": "Normal",
    "bold": "Bold",
    "italic": "Italic",
    "mono": "Mono",
}
FORMAT_LABELS = {"media": "Media", "document": "Document"}


def settings_keyboard(
    has_thumbnail: bool, caption_style: str | None, upload_format: str | None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"🖼 Thumbnail: {'Set' if has_thumbnail else 'Not Set'}",
            callback_data=SettingsCallback(action="thumb").pack(),
        ),
        InlineKeyboardButton(
            text="🗑 Delete",
            callback_data=SettingsCallback(action="delthumb").pack(),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=f"✏️ Caption: {CAPTION_LABELS.get(caption_style or 'normal', 'Normal')}",
            callback_data=SettingsCallback(action="caption").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"📁 Upload As: {FORMAT_LABELS.get(upload_format or '', 'Ask')}",
            callback_data=SettingsCallback(action="format").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🏠 Home", callback_data=UiCallback(action="home").pack()
        )
    )
    return builder.as_markup()


def format_keyboard(token: str, options: list[DownloadOption]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for option in options:
        builder.row(
            InlineKeyboardButton(
                text=option.label,
                callback_data=RequestCallback(
                    token=token, action=option.option_id
                ).pack(),
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="Close", callback_data=UiCallback(action="close").pack()
        )
    )
    return builder.as_markup()


def format_preference_keyboard(current: str | None) -> InlineKeyboardMarkup:
    def _label(value: str, title: str) -> str:
        return f"✅ {title}" if current == value else title

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=_label("document", "Document"),
            callback_data=FormatCallback(value="document").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=_label("media", "Media"),
            callback_data=FormatCallback(value="media").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=_label("ask", "Ask every time"),
            callback_data=FormatCallback(value="ask").pack(),
        )
    )
    return builder.as_markup()


def caption_style_keyboard(current: str | None) -> InlineKeyboardMarkup:
    active = current or "normal"

    def _label(value: str, title: str) -> str:
        return f"✅ {title}" if active == value else title

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=_label("normal", "Normal"),
            callback_data=CaptionStyleCallback(value="normal").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=_label("bold", "Bold"),
            callback_data=CaptionStyleCallback(value="bold").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=_label("italic", "Italic"),
            callback_data=CaptionStyleCallback(value="italic").pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=_label("mono", "Mono"),
            callback_data=CaptionStyleCallback(value="mono").pack(),
        )
    )
    return builder.as_markup()
