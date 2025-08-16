import os
import asyncio
import random
from aiogram.types import FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден!")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class QuestStates(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()

async def send_wrong_answer(message: types.Message):
    await message.answer("Любимая, это не то 🌸 попробуй ещё раз, я верю в тебя 💕")

# Словари с вариантами ответов
answers = {
    "q1": ["чат", "чат корши", "в чате", "в чате у корши"],
    "q2": ["комета", "холод", "киця кицюня"],
    "q3": ["всю меня", "личико", "глазки", "улыбочку", "тити", "ручки", "плечики", "губки", "носик", "щечки", "ножки", "фигурку"],
    "q4": ["ночь", "вечер", "поздно", "утром"],
    "q5": ["киця", "кицюня", "котёнок", "любимая", "солнышко", "моя девочка", "принцесса", "тасенька"],
    "q6": ["сердце", "сообщения", "голосовые", "песни", "сны", "мысли", "скучаешь", "фоточки", "все", "всё"],
    "q7": ["обняться", "поцеловаться", "обнимашки", "встретиться", "держаться за ручку", "туда сюда", "погулять", "спать вместе"],
    "q8": ["море", "париж", "киев", "казань", "весь мир", "владивосток", "уссурийск"],
    "q9": ["спокойной ночи", "самых сладеньких снов", "сладких снов", "люблю тебя", "кохаю тебе", "люблю тебя безумно сильно", "люблю тебя очень очень сильно", "ты самый самый лучший", "ты самая самая лучшая", "соскучился по тебе", "соскучилась по тебе"],
    "q10": ["сердце", "звезда", "луна", "розочка", "кольцо", "бесконечность", "сердечко", "котики", "выдрочки", "бибизянки", "обезьянки", "лебеди", "собачки"]
}

questions = {
    "q1": "✨ Первый вопрос: Где мы впервые встретились онлайн?",
    "q2": "🎶 Какая песня одна из первых, которую я тебе показал (или ту, которую я иногда тебе пою)?",
    "q3": "📸 Что я больше всего люблю видеть на твоих фоточках?",
    "q4": "🌙 В какое время суток мы чаще всего общаемся?",
    "q5": "💌 Какое моё любимое обращение к тебе?",
    "q6": "❤️ Что напоминает тебе обо мне каждый день?",
    "q7": "🤗 Что мы мечтаем сделать при встрече?",
    "q8": "🌍 Какое место мы обязательно посетим вдвоём?",
    "q9": "😴 Что мы чаще всего говорим друг другу перед сном?",
    "q10": "💖 Если бы у нас был общий символ, что бы это было?"
}

order = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]

# 📸 список фото
photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет, моя любимая Тасенька 💖 Готова пройти романтический квест о нашей истории? Напиши /начать")

@dp.message(F.text == "/начать")
async def start_quest(message: types.Message, state: FSMContext):
    await message.answer(questions["q1"])
    await state.set_state(QuestStates.q1)

# Обработчики вопросов
async def handle_answer(message: types.Message, state: FSMContext, current_q: str, next_q: str, next_state: State):
    text = message.text.lower()
    if any(ans in text for ans in answers[current_q]):
        if next_q:
            await message.answer(f"Правильно, любимая 🌹 {questions[next_q]}")
            await state.set_state(next_state)
 else:
    await message.answer("Ты справилась, моя душа! 🥰 Наш квест завершён, а наша история только начинается ✨")
    await message.answer("Хочу подарить тебе кое-что особенное... 🎁")
    try:
        photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]  # названия твоих фото
        chosen_photo = random.choice(photos)
        photo = FSInputFile(chosen_photo)
        await message.answer_photo(photo, caption="Это моё послание тебе, любовь моя 💖")
        except FileNotFoundError:
        await message.answer("Фото не найдено, но знай — в моём сердце всегда твои образы 💞")

# Динамическое создание хендлеров
@dp.message(QuestStates.q1)
async def q1(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q1", "q2", QuestStates.q2)

@dp.message(QuestStates.q2)
async def q2(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q2", "q3", QuestStates.q3)

@dp.message(QuestStates.q3)
async def q3(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q3", "q4", QuestStates.q4)

@dp.message(QuestStates.q4)
async def q4(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q4", "q5", QuestStates.q5)

@dp.message(QuestStates.q5)
async def q5(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q5", "q6", QuestStates.q6)

@dp.message(QuestStates.q6)
async def q6(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q6", "q7", QuestStates.q7)

@dp.message(QuestStates.q7)
async def q7(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q7", "q8", QuestStates.q8)

@dp.message(QuestStates.q8)
async def q8(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q8", "q9", QuestStates.q9)

@dp.message(QuestStates.q9)
async def q9(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q9", "q10", QuestStates.q10)

@dp.message(QuestStates.q10)
async def q10(message: types.Message, state: FSMContext):
    await handle_answer(message, state, "q10", None, None)

# HTTP-сервер для Render
async def handle(request):
    return web.Response(text="Бот работает! Это HTTP-сервер для Render.")

async def run_all():
    app = web.Application()
    app.router.add_get('/', handle)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=8080)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_all())



