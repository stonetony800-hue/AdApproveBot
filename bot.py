import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am the AdApproveBot.\n\n"
        "I am ready to manage advertisements."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message:
        return

    # Basic ad detection
    text = message.text or message.caption or ""

    ad_words = [
        "buy",
        "sell",
        "discount",
        "promo",
        "promotion",
        "advertise",
        "advertisement",
        "sale"
    ]

    if any(word in text.lower() for word in ad_words):
        await message.reply_text(
            "📢 Advertisement detected.\n"
            "This ad has been received for approval."
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CaptionRegex(".*"),
            handle_message
        )
    )

    print("AdApproveBot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
