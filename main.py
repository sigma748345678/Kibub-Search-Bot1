import telebot
from groq import Groq

# --- ТВОИ ДАННЫЕ (Вставь их сюда) ---
TELEGRAM_TOKEN = "8742380280:AAEgDs_NCFAWVas65cPVV7vmwM_2VbPTXgA"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот с ИИ, спрашивай что хочешь 🤖")


@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    try:
        # Показываем, что бот печатает
        bot.send_chat_action(message.chat.id, 'typing')

        # ЗАМЕНА МОДЕЛИ: llama-3.3-70b-versatile — это новая мощная версия
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}]
        )

        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Упс, возникла ошибка. Скорее всего, проблемы с API или интернетом.")


print("Бот запущен и ждет сообщений...")
bot.polling(none_stop=True)
