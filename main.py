import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден!")

# Полностью исправленная инициализация бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class QuestStates(StatesGroup):
    waiting_for_answer1 = State()
    waiting_for_answer2 = State()
    waiting_for_final_answer = State()

async def send_wrong_answer(message: types.Message):
    await message.answer("Аяяй, любимая моя девочка, похоже, ты не угадала, попробуй ещё раз, я уверен, что у тебя получится!💗")

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет! Готов начать квест? Напиши /начать")

@dp.message(F.text == "/начать")
async def question1(message: types.Message, state: FSMContext):
    await message.answer("Первая загадка: Где мы впервые поговорили?")
    await state.set_state(QuestStates.waiting_for_answer1)

@dp.message(QuestStates.waiting_for_answer1)
async def answer1(message: types.Message, state: FSMContext):
    if message.text.lower() == "чат корши":
        await message.answer("Правильно! Следующий вопрос: Как называется песня, которую я тебе однажды посвятил?")
        await message.answer("Запомни эти цифры: 12")
        await state.set_state(QuestStates.waiting_for_answer2)
    else:
        await send_wrong_answer(message)

@dp.message(QuestStates.waiting_for_answer2)
async def answer2(message: types.Message, state: FSMContext):
    if message.text.lower() in ["комета", "холод"]:
        await message.answer("Правильно! Финальный вопрос: Сколько раз мы сказали друг другу 'люблю тебя'?")
        await message.answer("Запомни эти цифры: 09")
        await state.set_state(QuestStates.waiting_for_final_answer)
    else:
        await send_wrong_answer(message)

@dp.message(QuestStates.waiting_for_final_answer)
async def final_question(message: types.Message, state: FSMContext):
    if message.text == "3323":
        await message.answer("Отлично! Теперь собери все цифры, которые я тебе отправил, и напиши дату, которую они образуют.")
        await message.answer("Запомни эти цифры: 23")
    else:
        await send_wrong_answer(message)

@dp.message(F.text == "12.09.23")
async def final_answer(message: types.Message):
    await message.answer("Ты справилась! 🎉 Поздравляю, ты раскрыла тайное послание! ❤️")
    await message.answer("Теперь, получи послание в видео формате!")

    try:
        video = InputFile("video.mp4")
        await message.answer_video(video)
    except FileNotFoundError:
        await message.answer("Ошибка: видео не найдено.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

