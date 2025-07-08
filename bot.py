import logging
import os
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

API_URL = "https://api.grok.x.ai/v1/chat/completions"
MODEL_NAME = "grok-3-mini-beta"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    await update.message.reply_text("سلام! پیام خود را بفرستید.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward user message to Grok API and return the response."""
    user_message = update.message.text

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": user_message},
        ],
    }

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except Exception as exc:
        logger.exception("Request to Grok failed: %s", exc)
        await update.message.reply_text("خطا در برقراری ارتباط. لطفاً دوباره تلاش کنید.")
        return

    if response.status_code == 200:
        try:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
        except Exception as exc:
            logger.exception("Invalid response: %s", exc)
            await update.message.reply_text("پاسخ نامعتبر از Grok دریافت شد.")
            return
        await update.message.reply_text(reply)
    elif response.status_code == 401:
        await update.message.reply_text("خطا: دسترسی نامعتبر است. لطفاً کلید Grok را بررسی کنید.")
    elif response.status_code >= 500:
        await update.message.reply_text("خطای سرور Grok. لطفاً بعداً امتحان کنید.")
    else:
        await update.message.reply_text(f"خطای نامشخص ({response.status_code}).")


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()
