from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "foydalanuvchi"
    await update.message.reply_text(
        f"👋 Salom, {user}!\n"
        "📥 Menga Instagram video link yuboring."
    )

# Instagram video yuklab olish
async def handle_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id

    if "instagram.com" not in url:
        await update.message.reply_text("❌ Faqat Instagram link yuboring.")
        return

    await update.message.reply_text("⏳ Video yuklanmoqda...")

    try:
        ydl_opts = {
            'outtmpl': 'insta.%(ext)s',
            'format': 'best',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        filesize = os.path.getsize(filename)

        if filesize <= 50 * 1024 * 1024:  # 50 MB
            await context.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'))
        else:
            await update.message.reply_text("⚠️ Video 50 MB dan katta, uzr.")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik yuz berdi:\n{str(e)}")

# 🔑 Bot tokeningiz
TOKEN = "7674629095:AAG3kCTMiooj0rgD--WxeVmPyxPEVglIJ84"

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram))

print("🤖 @instavideoxbot ishga tushdi!")
app.run_polling()
