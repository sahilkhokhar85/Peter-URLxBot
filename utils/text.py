START_TEXT = """<b>Hi {mention}!!</b>

<blockquote><b>I'm URL Uploader Bot. Just send me any Direct download link and I'll upload file remotely to Telegram.</b></blockquote>"""

HELP_TEXT = """<b>📖 Help!!</b>

<b>Send me any direct link and I'll upload it to Telegram.
Custom name: link|filename</b>

<blockquote><b>/rename - rename telegram files
/convert2file - upload as document
/convert2video - upload as video
/settings - change bot settings
/set_caption - set default caption
/set_thumb - set default thumbnail
/delete_thumb - delete default thumbnail</b></blockquote>

<b>Don't forget to check bot settings</b>"""

SETTINGS_TEXT = "<b>⚙️ Here you can change bot settings!!</b>"


def about_text(active: int, total: int, banned: int, uptime: str) -> str:
    return (
        "<b>📰 About!!</b>\n\n"
        "<blockquote>"
        "<b>📝 Language:</b> Python 3\n"
        "<b>🧰 Framework:</b> Aiogram 3\n"
        "<b>📥 Downloader:</b> yt-dlp\n\n"
        f"<b>🔥 Active users:</b> {active} in last 24 hrs\n"
        f"<b>👥 Total users:</b> {total}\n"
        f"<b>🚫 Banned users:</b> {banned}\n\n"
        f"<b>⏱ Uptime:</b> {uptime}"
        "</blockquote>"
    )


THUMB_SAVED = "Your custom thumbnail is saved."
THUMB_MISSING = "You do not have a thumbnail yet. Send a JPG image to save one."
THUMB_REMOVED = "Your thumbnail was removed successfully."

PROCESSING = "Processing your link..."
FORMAT_SELECTION = "Choose the format you want."
DOWNLOAD_START = "Downloading <b>{name}</b>"
UPLOAD_START = "Uploading <b>{name}</b>"
QUICK_CHOICE = "Choose how you want this YouTube link downloaded."
YOUTUBE_AUDIO_LABEL = "Audio"
YOUTUBE_VIDEO_LABEL = "Video"
RATE_LIMIT = (
    "Please wait before starting another request. Try again in about {minutes} minute(s)."
)
DOWNLOAD_FAILED = "I could not process that link."
DIRECT_DOWNLOAD_FAILED = "I could not download that file."
REQUEST_EXPIRED = "That request has expired. Send the link again."
FILE_TOO_LARGE = (
    "Downloaded in {seconds} seconds.\nDetected file size: {size}\n"
    "I cannot upload files larger than Telegram allows."
)
DONE = "Downloaded in {download_seconds} seconds.\nUploaded in {upload_seconds} seconds."


def upload_caption(name: str) -> str:
    return UPLOAD_START.format(name=name)


def download_caption(name: str) -> str:
    return DOWNLOAD_START.format(name=name)
