from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest
from app.config import settings
from datetime import date

from app.services.stats import get_daily_stats
from app.db import SessionLocal
from app.models import Parent # Parent modelini import qildik

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Salom! Men Face-ID davomat botiman.\n"
            "Direktor bo'lsangiz, /stat buyrug'ini yuboring.\n"
            "Ota-ona bo'lsangiz, sizga berilgan maxsus kodni yuboring."
        )

# --- OTA-ONANI RO'YXATDAN O'TKAZISH ---
async def handle_parent_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    code = update.message.text.strip().upper()
    db = SessionLocal()
    
    try:
        # Bazadan ota-onani kod bo'yicha qidiramiz
        parent = db.query(Parent).filter(Parent.link_code == code).first()
        
        if parent:
            # Chat ID ni saqlab qo'yamiz
            parent.telegram_chat_id = update.effective_chat.id
            db.commit()
            await update.message.reply_text(f"✅ Tasdiqlandi!\nSiz {parent.full_name} sifatida ro'yxatdan o'tdingiz.")
        else:
            # Agar kod bazada bo'lmasa yoki xato bo'lsa
            await update.message.reply_text("❌ Xato kod yoki bunday ota-ona tizimda mavjud emas.")
    finally:
        db.close()

# --- STATISTIKA KOMANDASI ---
async def stat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        stats = get_daily_stats(db)
        text = (
            f"📊 **KUNLIK DAVOMAT HISOBOTI**\n"
            f"🗓 Sana: {date.today()}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 Jami o'quvchilar: {stats['total']}\n"
            f"✅ Kelganlar: {stats['present']}\n"
            f"❌ Kelmaganlar: {stats['absent']}\n"
            f"📈 Davomat ko'rsatkichi: {stats['percent']}%"
        )
        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown")
    finally:
        db.close()

def build_bot():
    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
    )

    app = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token.strip())
        .request(request)
        .build()
    )

    # Handlerlarni qo'shamiz
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stat", stat_command))
    
    # MATNLI XABARLAR UCHUN (Kodni ushlab olish)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_parent_code))
    
    return app

application = build_bot()
bot = application.bot

if __name__ == "__main__":
    print("Telegram bot ishga tushdi...")
    application.run_polling()
