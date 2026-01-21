from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.config import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "Salom! Bog‘lanish uchun admin bergan link code ni yuboring."
    )


def build_bot():
    app = ApplicationBuilder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    return app


if __name__ == "__main__":
    bot = build_bot()
    bot.run_polling()
