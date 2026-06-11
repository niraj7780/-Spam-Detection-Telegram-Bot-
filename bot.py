import os
import re
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ✅ TOKEN
TOKEN = os.getenv("TOKEN")

# ✅ Fake server (Render FREE)
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

# ✅ BUTTON MENU
def get_menu():
    keyboard = [
        ["🛡 Check Message", "🔗 Check Link"],
        ["📊 Scan SMS", "ℹ About Bot"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ✅ START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Niraj Spam Shield Bot\n\n"
        "Choose option 👇",
        reply_markup=get_menu()
    )

# ✅ KEYWORDS (AI logic)
SPAM_WORDS = [
    "win", "free", "prize", "lottery", "click", "urgent",
    "verify", "account", "offer", "money", "reward", "congratulations"
]

SUSPICIOUS_LINKS = [
    "bit.ly", "tinyurl", "shorturl", "goo.gl", "grabify"
]

# ✅ ANALYSIS FUNCTION (AI)
def analyze_text(text):
    text = text.lower()

    score = 0

    # ✅ keyword scoring
    for word in SPAM_WORDS:
        if word in text:
            score += 1

    # ✅ link detection
    links = re.findall(r'https?://\S+', text)

    for link in links:
        for bad in SUSPICIOUS_LINKS:
            if bad in link:
                score += 2

    # ✅ decision
    if score >= 3:
        return "🚨 SPAM", "High risk message\nDo not click links ❌"
    elif score >= 1:
        return "⚠ Suspicious", "Be careful ⚠"
    else:
        return "✅ Safe", "No threat found ✅"

# ✅ BUTTON HANDLER
user_mode = {}

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "🛡 Check Message":
        user_mode[user_id] = "message"
        await update.message.reply_text("Send message to scan 📩")

    elif text == "🔗 Check Link":
        user_mode[user_id] = "link"
        await update.message.reply_text("Send link 🔗")

    elif text == "📊 Scan SMS":
        user_mode[user_id] = "sms"
        await update.message.reply_text("Send SMS text 📱")

    elif text == "ℹ About Bot":
        await update.message.reply_text(
            "👨‍💻 Niraj Charpe\n"
            "🛡 Spam Detection Bot\n"
            "🤖 AI-Based Message Scanner\n"
            "🚀 Built in Python"
        )

    else:
        # ✅ Process user input
        mode = user_mode.get(user_id, "message")

        result, info = analyze_text(text)

        await update.message.reply_text(
            f"{result}\n\n{info}"
        )

# ✅ MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("✅ Spam Shield Bot Running...")

    app.run_polling()

if __name__ == "__main__":
    main()
