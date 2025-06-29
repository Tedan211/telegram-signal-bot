import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

long_keywords = ["long", "多", "做多"]
short_keywords = ["short", "空", "做空"]

def classify_signal(text):
    text_lower = text.lower()
    for word in long_keywords:
        if word in text_lower:
            return "📈 偵測到【多單】訊號"
    for word in short_keywords:
        if word in text_lower:
            return "📉 偵測到【空單】訊號"
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text or ""
    user = update.message.from_user.username or update.message.from_user.first_name
    result = classify_signal(msg)

    if result:
        response = f"👤 來源：@{user}\n📨 訊號：{msg}\n➡️ 分類：{result}"
        await update.message.reply_text(response)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("✅ Bot 已啟動，正在監聽訊息...")
app.run_polling()
