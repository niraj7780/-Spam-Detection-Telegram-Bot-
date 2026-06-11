import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

# ✅ Fake server (Render free)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Spam Bot Running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

# ✅ Button UI
def menu():
    keyboard = [
        ["🛡 Check Message", "🔗 Check Link"],
        ["📱 Scan SMS", "ℹ About"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ✅ Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Niraj Spam Shield Bot\n\nChoose option 👇",
        reply_markup=menu()
    )

# ✅ AI Logic
SPAM_WORDS = [
    "win", "free", "prize", "lottery", "click", "urgent",
    "verify", "account", "offer", "money", "reward"
]

BAD_LINKS = [
    "bit.ly", "tinyurl", "goo.gl", "shorturl"
]

def analyze(text):
    text = text.lower()
    score = 0

    # keyword check
    for word in SPAM_WORDS:
        if word in text:
            score += 1

    # link check
    links = re.findall(r'https?://\S+', text)
    for link in links:
        for bad in BAD_LINKS:
            if bad in link:
                score += 2

    # result
    if score >= 3:
        return "🚨 SPAM", "High risk! Do not click ❌"
    elif score >= 1:
        return "⚠ Suspicious", "Be careful ⚠"
    else:
        return "✅ Safe", "No threat ✅"

# ✅ Handle buttons + input
user_mode = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # button selection
    if text in ["🛡 Check Message", "🔗 Check Link", "📱 Scan SMS"]:
        user_mode[user_id] = "check"
        await update.message.reply_text("Send your text or link ✅")
        return

    elif text == "ℹ About":
        await update.message.reply_text(
            "👨‍💻 Niraj Charpe\n"
            "🛡 Spam Detection Bot\n"
            "🤖 AI based scanner"
        )
        return

    # process input
    result, info = analyze(text)

    await update.message.reply_text(
        f"{result}\n\n{info}"
    )

# ✅ Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("✅ Spam Bot Running...")

    app.run_polling()

if __name__ == "__main__":
    main()
