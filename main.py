import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🚨 CONFIGURATION: Replace these placeholders with your actual values
VIDEO_FILE_ID = "BAACAgQAAxkBAAMDakZaJrWHMbEfyvEeDtA2E6tKcv0AAtEdAAJmtjhSFJfiaJ62xu88BA"
CHANNEL_URL = "https://t.me/PrimeForex1121"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "📊 **Welcome to AuraForex Analytics Core**\n\n"
        "Your automated dashboard for market execution metrics, currency tracking utilities, "
        "and volatility calculation analytics.\n\n"
        "💡 *Select an educational market tool module below to begin:* \n\n"
        "⚠️ *Disclaimer: This platform provides educational market utilities only. "
        "Content does not constitute financial, trading, or investment advice.*"
    )
    
    # Grid layout adding the channel link cleanly at the very top of the interface options
    keyboard = [
        [InlineKeyboardButton("📢 Join Our Telegram Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("🧰 Position Size Calculator", callback_data="calc")],
        [InlineKeyboardButton("📈 Volatility Indicators", callback_data="volatility")],
        [InlineKeyboardButton("📚 Educational Resources", callback_data="edu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Using reply_video attaches the media asset alongside your button panel layout
    try:
        await update.message.reply_video(
            video=VIDEO_FILE_ID,
            caption=welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Media welcome processing failed: {e}")
        # Secure safety fallback if video reference is momentarily unavailable during deployment
        await update.message.reply_text(
            text=welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def button_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Back option to return to the original menu screen cleanly
    if query.data == "back_to_menu":
        welcome_text = (
            "📊 **Welcome to AuraForex Analytics Core**\n\n"
            "Select an educational market tool module below to begin:"
        )
        keyboard = [
            [InlineKeyboardButton("📢 Join Our Telegram Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("🧰 Position Size Calculator", callback_data="calc")],
            [InlineKeyboardButton("📈 Volatility Indicators", callback_data="volatility")],
            [InlineKeyboardButton("📚 Educational Resources", callback_data="edu")]
        ]
        await query.edit_message_caption(caption=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    # Sub-menu button states
    if query.data == "calc":
        calc_text = (
            "🧰 **Risk & Position Size Calculator**\n"
            "---\n"
            "Plan your market exposures safely using standard risk parameters:\n\n"
            "• **Standard Lot size:** 100,000 units\n"
            "• **Mini Lot size:** 10,000 units\n"
            "• **Micro Lot size:** 1,000 units\n\n"
            "👉 *To calculate your exact lot size, use formula:* \n"
            "$$Lot = \\frac{Risk\\ Amount}{(Stop\\ Loss\\ in\\ Pips \\times Pip\\ Value)}$$"
        )
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_menu")]]
        await query.edit_message_caption(caption=calc_text, reply_markup=InlineKeyboardMarkup(back_keyboard), parse_mode="Markdown")

    elif query.data == "volatility":
        vol_text = (
            "📈 **Market Volatility Mechanics**\n"
            "---\n"
            "Tracking currency pair volatility is crucial for setting protective stop losses.\n\n"
            "📊 **Average True Range (ATR) Baselines:**\n"
            "• EUR/USD: 60-80 pips daily avg.\n"
            "• GBP/JPY: 120-150 pips daily avg.\n"
            "• Gold (XAU/USD): 200-300 pips daily avg.\n\n"
            "💡 *Tip: High volatility pairs require wider parameters to avoid premature stop-outs.*"
        )
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_menu")]]
        await query.edit_message_caption(caption=vol_text, reply_markup=InlineKeyboardMarkup(back_keyboard), parse_mode="Markdown")

    elif query.data == "edu":
        edu_text = (
            "📚 **Forex Market Academy Modules**\n"
            "---\n"
            "Master the foundational elements of data structures in trading:\n\n"
            "1️⃣ **Technical Analysis:** Reading candlestick chart syntax, trendlines, and breakouts.\n"
            "2️⃣ **Risk Management:** Never exposing more than 1% to 2% of total capital on a single transaction setup.\n"
            "3️⃣ **Fundamental Data:** Monitoring macroeconomic interest rates, NFP releases, and central bank policies."
        )
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_to_menu")]]
        await query.edit_message_caption(caption=edu_text, reply_markup=InlineKeyboardMarkup(back_keyboard), parse_mode="Markdown")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_dispatcher))
    application.run_polling()

if __name__ == "__main__":
    main()
