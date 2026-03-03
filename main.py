import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ ---
TELEGRAM_TOKEN = "8742380280:AAEgDs_NCFAWVas65cPVV7vmwM_2VbPTXgA"
GROQ_API_KEY = "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"

# --- ВЕБ-СЕРВЕР (Flask) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает! 🤖"

def run():
    # Запускаем сервер на порту 8080
    app.run(host='0.0.0.0', port=8080)

# Запускаем Flask в отдельном потоке, чтобы он не мешал боту
Thread(target=run).start()

# --- ЛОГИКА БОТА ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот с ИИ, теперь я онлайн 24/7. Спрашивай! 🤖")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Используем актуальную модель llama-3.3-70b-versatile
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}]
        )
        
        answer = response.choices[0].message.content
        bot.send_message(message.chat.id, answer)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка в нейросети. Попробуй позже.")

# Запуск бота
if __name__ == "__main__":
    print("Веб-сервер запущен. Бот начинает опрос...")
    bot.polling(none_stop=True)
