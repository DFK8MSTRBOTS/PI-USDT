
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Salut! Le bot est actif et fonctionne sur Render!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
import os

ASK_NAME, ASK_FEELING = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Salut toi 😏 Comment tu t'appelles?")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text(f"Enchanté, {update.message.text}. Comment tu te sens aujourd’hui?")
    return ASK_FEELING

async def ask_feeling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    feeling = update.message.text
    name = context.user_data.get("name", "toi")

    if "bien" in feeling.lower():
        reply = f"Je suis contente pour toi, {name} 😊 Tu veux jaser un peu?"
    elif "mal" in feeling.lower() or "pas bien" in feeling.lower():
        reply = f"Oh non 😔 Veux-tu m’en parler, {name}?"
    else:
        reply = f"Intéressant... Tu veux que je te change les idées, {name}?"

    await update.message.reply_text(reply)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("D'accord, on arrête ici. Mais reviens me jaser, ok? 😉")
    return ConversationHandler.END

if __name__ == '__main__':
    import asyncio

    TOKEN = os.getenv("TELEGRAM_TOKEN")  # ou écris ton token directement ici
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_FEELING: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_feeling)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    # Démarre le bot
    print("Bot démarré...")
    asyncio.run(app.run_polling())
