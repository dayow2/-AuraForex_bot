import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Setup Logging to observe actions in the Railway console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Extract configuration from Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
# NOTE: Once you find your Video File ID using the step below, paste it here!
VIDEO_FILE_ID = os.getenv("VIDEO_FILE_ID", "PASTE_YOUR_TELEGRAM_VIDEO_FILE_ID_HERE")
CHANNEL_URL = "https://t.me/PrimeForex1121"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the welcome message, video, and your channel access button."""
    welcome_text = (
        "📊 *Welcome to PrimeForex Bot!*\n\n"
        "Unlock elite Forex insights, real-time market analysis, and precision signals "
        "designed to scale your trading parameters.\n\n"
        "🚀 Click the button below to join our official trading feed!"
    )
    
    # Create the beautiful interactive button linking to your Forex channel
    keyboard = [[InlineKeyboardButton("🎯 Join PrimeForex Channel", url=CHANNEL_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # Attempt to deliver using the efficient Telegram file_id cache
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=VIDEO_FILE_ID,
            caption=welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Failed to send video: {e}. Falling back to plain text welcome.")
        # Fail-safe alternative if your file_id isn't filled out or configured yet
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{welcome_text}\n\n_(Note: Video configuration pending setup)_",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def catch_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helper Function: Logs incoming video IDs to your terminal logs."""
    if update.message.video:
        file_id = update.message.video.file_id
        logger.info(f"!!! FOUND YOUR VIDEO FILE ID !!! -> {file_id}")
        await update.message.reply_text(
            f"✅ **Video ID Captured!**\n\nCopy this exact ID and save it:\n`{file_id}`",
            parse_mode="Markdown"
        )

def main() -> None:
    """Pre-initializes the Telegram Application loop."""
    if not TOKEN:
        logger.error("CRITICAL ERROR: BOT_TOKEN environment variable is missing!")
        return

    # Build the bot runtime application instance
    application = Application.builder().token(TOKEN).build()

    # Match commands and standard user inputs
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, catch_video_id))

    # Keep polling for user actions indefinitely
    logger.info("PrimeForex Bot Engine Started Successfully...")
    application.run_polling()

if __name__ == '__main__':
    main()
