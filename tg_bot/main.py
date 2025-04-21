import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    CommandHandler,
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = context.args[0] if context.args else None
    redirect_url = os.getenv("TELEGRAM_BOT_REDIRECT_URL")
    logger.info(f"Redirecting to {redirect_url}")
    logger.info(f"Token: {token}")
    if token:
        response = requests.post(
            redirect_url,
            json={
                "telegram_id": update.effective_user.id,
                "telegram_first_name": update.effective_user.first_name,
                "telegram_last_name": update.effective_user.last_name,
                "telegram_username": update.effective_user.username,
                "auth_token": token,
            },
        )
        if response.status_code == 200:
            await update.message.reply_text("Вы успешно авторизовались!")
        else:
            await update.message.reply_text("Ошибка авторизации.")
    else:
        await update.message.reply_text("Токен не найден.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получено сообщение:{update.message.text}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
