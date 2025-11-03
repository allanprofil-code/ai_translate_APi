import telebot
import requests
import os

BOT_TOKEN = os.getenv("8439525451:AAEX7rNJm1YByVN0Gslf48T4-PfG21T2TAs")
TILMOCH_API_KEY = os.getenv("th_8a4a73d1-07ad-4b3b-932a-0d2a8a2fc4d5")

bot = telebot.TeleBot(BOT_TOKEN)

def translate_text(text, source_lang="en", target_lang="ka"):
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
    kaa = translate_text(text, "en", "ka")

    result = f"🇺🇸 English: {text}\n\n🇺🇿 Uzbek: {uz}\n\n🏴 Qaraqalpaq: {ka}"
    bot.send_message(message.chat.id, result)

print("🤖 Bot ishga tushdi...")
bot.polling()
