import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
TILMOCH_API_KEY = os.getenv("TILMOCH_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

def translate_text(text, source_lang="eng_Latn", target_lang="kaa_Latn"):
    url = "https://websocket.tahrirchi.uz/translate-v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": TILMOCH_API_KEY
    }
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "model": "tilmoch"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"⚠️ API xato kodi: {response.status_code}"

        data = response.json()
        return data.get("translated_text", "⚠️ Tarjima topilmadi.")
    except Exception as e:
        return f"⚠️ Xato: {e}"

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    text = message.text
    bot.reply_to(message, "⏳ Tarjima qilinmoqda...")

    uz = translate_text(text, "eng_Latn", "uzn_Latn")
    kaa = translate_text(text, "eng_Latn", "kaa_Latn")

    result = (
        f"🇺🇸 English: {text}\n\n"
        f"🇺🇿 Uzbek: {uz}\n\n"
        f"🏴 Qaraqalpaq: {kaa}"
    )

    bot.send_message(message.chat.id, result)

print("🤖 Bot Railway’da ishga tushdi...")
bot.polling()
