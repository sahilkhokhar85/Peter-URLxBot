START_TEXT = """<b>Hi {mention}!

I'm URL Uploader Bot. Just send me any Direct download link and I'll upload file remotely to Telegram.</b>"""

HELP_TEXT = """<b>📖 Help

Following are the commands and their descriptions:

/rename - rename telegram files
/convert2file - upload as document
/convert2video - upload as video
/settings - change bot settings
/set_caption - set default caption
/set_thumb - set default thumbnail
/delete_thumb - delete default thumbnail

Send any direct link to start. Custom name: link|filename

Don't forget to check bot settings</b>"""

ABOUT_TEXT = """<b>📰 About

📝 Language: Python 3
🧰 Framework: Aiogram 3</b>"""

# Invisible character (U+2800) so the Settings screen shows only buttons.
SETTINGS_TEXT = "\u2800"

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
