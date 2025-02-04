import sqlite3
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime

# Token del bot (reemplaza con el tuyo)
BOT_TOKEN = "7562287893:AAEZqm9cTrGr6Yfk7vXp75MPd5yA76lZT2c"
IMGFLIP_API_URL = "https://api.imgflip.com/caption_image"
# Credenciales de Imgflip
IMGFLIP_USERNAME = "Agmatar"
IMGFLIP_PASSWORD = "HUreqm5HiRqOwnrfpYcy"

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect("memes.db") # creates a database called memes.db
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meme_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """) # creates a table called memes
    conn.commit()
    conn.close()

async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_text(
        f"¡Hola {user.first_name}! 👋 Bienvenido al Oráculo Memeístico. "
        f"Prueba el comando /azar para obtener un meme aleatorio."
    )

async def meme_azar(update: Update, context):
    # Datos de ejemplo para el meme
    meme_template_id = "112126428"  # "Distracted Boyfriend" template
    text0 = "Yo aprendiendo bots"
    text1 = "Mi vida social"

    # Solicitud a Imgflip API
    params = {
        "template_id": meme_template_id,
        "username": IMGFLIP_USERNAME,
        "password": IMGFLIP_PASSWORD,
        "text0": text0,
        "text1": text1,
    }

    response = requests.post(IMGFLIP_API_URL, params=params)
    data = response.json()

    if data["success"]:
        meme_url = data["data"]["url"]

        # Guardar en la base de datos
        save_meme(meme_url)

        await update.message.reply_photo(photo=meme_url)
    else:
        await update.message.reply_text("Hubo un problema generando el meme 😢")

def save_meme(meme_url):
    conn = sqlite3.connect("memes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memes (meme_url) VALUES (?)", (meme_url,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Inicializar la base de datos
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("azar", meme_azar))

    print("🤖 Bot en funcionamiento...")
    app.run_polling()