import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import DDGS

TOKEN = "8303799209:AAHTHtM6Hy437kNYPLNbVu51kRwL7gLnUMU"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🔎 Привет! я ищу максимально строго..")


@dp.message(F.text)
async def search_handler(message: types.Message):
    if message.text.startswith('/'): return

    status_msg = await message.answer("📡 Ищу...")
    # Убираем лишние пробелы и переводим в нижний регистр
    query = message.text.lower().strip()
    query_words = query.split()

    try:
        valid_results = []

        with DDGS() as ddgs:
            # Ищем чуть больше (15), чтобы была выборка для фильтра
            # Добавим регистр и попробуем заставить его искать на русском
            raw = ddgs.text(query, region='ru-ru', max_results=20)

            for r in raw:
                title = r['title'].lower()
                body = r['body'].lower()

                # СТРОГАЯ ПРОВЕРКА: ищем именно вхождение слов запроса
                # Если хоть одно слово из запроса есть в заголовке или описании
                if any(word in title or word in body for word in query_words):
                    safe_title = r['title'].replace('<', '').replace('>', '')
                    safe_body = r['body'].replace('<', '').replace('>', '')

                    valid_results.append(f"🔹 <b>{safe_title}</b>\n{safe_body}\n🔗 {r['href']}")

                if len(valid_results) >= 5:
                    break

        # ВЫРУБАЕМ спам: если фильтр ничего не пропустил, не показываем ничего лишнего
        if not valid_results:
            await status_msg.edit_text(
                f"❌ По запросу «{message.text}» ничего релевантного не найдено. Попробуй уточнить запрос (например: 'кот животное').")
            return

        response = f"✅ Результаты для «{message.text}»:\n\n" + "\n\n".join(valid_results)

        if len(response) > 4000:
            response = response[:4000] + "..."

        await status_msg.edit_text(response, parse_mode="HTML", disable_web_page_preview=False)

    except Exception as e:
        print(f"Ошибка: {e}")
        await status_msg.edit_text("⚠️ Ошибка поиска. Попробуй позже.")


# Запуск одной строкой без main
asyncio.run(dp.start_polling(bot))
