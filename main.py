import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from duckduckgo_search import DDGS

TOKEN = "8402362105:AAFJzLPB6_7WJ9UhRiGQW_i9EgSscHJmq2k"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🔎 Привет! Пиши запрос.")


@dp.message(F.text)
async def search_handler(message: types.Message):
    if message.text.startswith('/'): return

    status_msg = await message.answer("📡 Ищу...")
    query_words = message.text.lower().split()

    try:
        valid_results = []
        raw_fallback = []

        with DDGS() as ddgs:
            raw = ddgs.text(message.text, region='ru-ru', max_results=10)

            for r in raw:
                # ИСПОЛЬЗУЕМ HTML-теги <b> вместо Markdown **
                # Также убираем символы < и >, чтобы Telegram не принял их за теги
                safe_title = r['title'].replace('<', '').replace('>', '')
                safe_body = r['body'].replace('<', '').replace('>', '')

                result_text = f"🔹 <b>{safe_title}</b>\n{safe_body}\n🔗 {r['href']}"

                raw_fallback.append(result_text)

                title_lower = r['title'].lower()
                body_lower = r['body'].lower()

                if any(word in title_lower or word in body_lower for word in query_words):
                    valid_results.append(result_text)

                if len(valid_results) >= 5:
                    break

        if not valid_results:
            valid_results = raw_fallback[:5]

        if not valid_results:
            await status_msg.edit_text("❌ Вообще ничего не нашлось по этому запросу.")
            return

        response = f"✅ Результаты для «{message.text}»:\n\n" + "\n\n".join(valid_results)

        if len(response) > 4000:
            response = response[:4000] + "..."

        # МЕНЯЕМ parse_mode НА HTML
        await status_msg.edit_text(response, parse_mode="HTML", disable_web_page_preview=False)

    except Exception as e:
        # ТЕПЕРЬ ОШИБКА БУДЕТ ВИДНА В КОНСОЛИ (ТЕРМИНАЛЕ)
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        await status_msg.edit_text("⚠️ Ошибка поиска.")


asyncio.run(dp.start_polling(bot))
