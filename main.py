from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Token del bot (reemplaza con el tuyo)
BOT_TOKEN = "7562287893:AAEZqm9cTrGr6Yfk7vXp75MPd5yA76lZT2c"

# Función para el comando /start
async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_text(
        f"¡Hola {user.first_name}! 👋 Bienvenido al Oráculo Memeístico. ¡Pronto estaremos generando risas!"
    )

if __name__ == "__main__":
    # Crear la aplicación del bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Registrar el comando /start
    app.add_handler(CommandHandler("start", start))

    # Iniciar el bot
    print("🤖 Bot en funcionamiento...")
    app.run_polling()
