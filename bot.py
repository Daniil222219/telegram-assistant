from telethon import TelegramClient, events
from dotenv import load_dotenv
from openai import OpenAI
import os

# Загружаем переменные из .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Создаем клиентов
gpt = OpenAI(api_key=openai_api_key)
telegram = TelegramClient(session_name, api_id, api_hash)

# ID "Избранного" чата (у Telegram у самого себя это 777000)
FAVORITE_CHAT_ID = 831884967

# Обработка входящих сообщений
@telegram.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        user_message = event.message.message
        sender = await event.get_sender()
        sender_name = sender.first_name if sender else "Неизвестный"
        print(f"[Получено сообщение от {sender_name}]: {user_message}")

        # Уведомление себе в "Избранное"
        await telegram.send_message(FAVORITE_CHAT_ID, f"Бот начал переписку с пользователем {sender_name}:
{user_message}")

        # Запрос к OpenAI
        response = gpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — иллюзионист Даниил Багинский. Общайся от первого лица, с уверенностью, харизмой и лёгким юмором. "
                        "Ты продаёшь шоу, задаёшь правильные вопросы, вовлекаешь клиента, предлагаешь доп. опции и мягко переводишь на звонок. "
                        "Отвечай так, как отвечает сам Даниил — профессионально, но живо и стильно."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        reply = response.choices[0].message.content
        print(f"[Ответ бота]: {reply}\n")
        await event.respond(reply)

# Запуск Telegram-клиента
telegram.start()
print("Ассистент Багинского запущен.")
telegram.run_until_disconnected()
