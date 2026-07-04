import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Premium, compliant welcome message avoiding "get rich" words
    welcome_text = (
        "📊 **Welcome to AuraForex Analytics Core**\n\n"
        "Your automated dashboard for market execution metrics, currency tracking utilities, "
        "and volatility calculation analytics.\n\n"
        "💡 *Select an educational market tool module below to begin:* \n\n"
        "⚠️ *Disclaimer: This platform provides educational market utilities only. "
        "Content does not constitute financial, trading, or investment advice.*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🧰 Position Size Calculator", callback_data="calc")],
        [InlineKeyboardButton("📈 Volatility Indicators", callback_data="volatility")],
        [InlineKeyboardButton("📚 Educational Resources", callback_data="edu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

async def button_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

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
        await query.edit_message_text(calc_text, parse_mode="Markdown")

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
        await query.edit_message_text(vol_text, parse_mode="Markdown")

    elif query.data == "edu":
        edu_text = (
            "📚 **Forex Market Academy Modules**\n"
            "---\n"
            "Master the foundational elements of data structures in trading:\n\n"
            "1️⃣ **Technical Analysis:** Reading candlestick chart syntax, trendlines, and structure breakouts.\n"
            "2️⃣ **Risk Management:** Never exposing more than 1% to 2% of total capital on a single transaction setup.\n"
            "3️⃣ **Fundamental Data:** Monitoring macroeconomic interest rates, NFP releases, and central bank policies."
        )
        await query.edit_message_text(edu_text, parse_mode="Markdown")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_dispatcher))
    application.run_polling()

if __name__ == "__main__":
    main()
