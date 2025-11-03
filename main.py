import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
TILMOCH_API_KEY = os.getenv("TILMOCH_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

def translate_text(text, source_lang="en", target_lang="kaa"):
    url = "https://tilmoch.ai/api/translate"
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "api_key": TILMOCH_API_KEY
    }

    try:
        response = requests.post(url, json=payload)
        print("🔹 API STATUS:", response.status_code)
        print("🔹 API RESPONSE:", response.text)

        if response.status_code != 200:
            return f"⚠️ API xato kodi: {response.status_code}"

        data = response.json()
        translated_text = data.get("translated_text")

        if not translated_text:
            return "⚠️ API javobida tarjima topilmadi."

        return translated_text

    except Exception as e:
        return f"⚠️ Xato: {e}"

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    text = message.text
    if not text:
        bot.reply_to(message, "Iltimos, matn yuboring.")
        return

    bot.reply_to(message, "⏳ Tarjima qilinmoqda...")

    uz = translate_text(text, "en", "uz")
    kaa = translate_text(text, "en", "kaa")

    result = (
        f"🇺🇸 English: {text}\n\n"
        f"🇺🇿 Uzbek: {uz}\n\n"
        f"🏴 Qaraqalpaq: {kaa}"
    )

    bot.send_message(message.chat.id, result)

print("🤖 Bot ishga tushdi...")
bot.polling()
