import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AdApproveBot is running!")

    def log_message(self, format, *args):
        return


def start_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am AdApproveBot.\n\n"
        "I am online and ready to manage advertisements."
    )


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    message = update.message

    if not message:
        return

    text = message.text or message.caption or ""

    ad_words = [
        "buy",
        "sell",
        "discount",
        "promo",
        "promotion",
        "advertise",
        "advertisement",
        "sale",
    ]

    if any(word in text.lower() for word in ad_words):
        await message.reply_text(
            "📢 Advertisement detected.\n"
            "This ad has been received for approval."
        )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    threading.Thread(
        target=start_web_server,
        daemon=True
    ).start()

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
