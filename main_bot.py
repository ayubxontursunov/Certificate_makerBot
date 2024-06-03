import logging
from config import API_Token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from creating_certificate import creating_func
from aiogram.types import InputFile

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FsmAdmin(StatesGroup):
    fullname = State()
    course = State()
    mark = State()
    finish = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Assalomu Alaykum, Certificate botiga xush kelibsiz!\nSertifikatga ega bo'lish uchun /certificate komandasidan foydalaning.\nPowered by Darko.")


@dp.message_handler(commands=['certificate'])
async def start_fsm(message: types.Message):
    await message.answer("Sertifakat olish uchun malumotlaringizni botga jo'nating.\nTo'liq ismingizni kiriting:")
    await FsmAdmin.fullname.set()


@dp.message_handler(state=FsmAdmin.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fullname"] = message.text.strip()
    await message.answer("Kursingizni kiriting: ")
    await FsmAdmin.next()


@dp.message_handler(state=FsmAdmin.course)
async def get_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["course"] = message.text.strip()
    await message.answer("O'zlashtirish darajangizni kiriting (1-100): ")
    await FsmAdmin.next()


@dp.message_handler(state=FsmAdmin.mark)
async def get_mark(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["mark"] = message.text.strip()
    await message.answer("Ma'lumotlaringiz qabul qilindi. Sertifikatni olish uchun 'Tugatish' ni yozing.")
    await FsmAdmin.next()


@dp.message_handler(state=FsmAdmin.finish)
async def finsh_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data["fullname"], data['course'], data['mark'])
        creating_func(data["fullname"], data['course'], data['mark'])
        my_document = InputFile(f'media/certificates/{data["fullname"]}.png')
    await bot.send_document(chat_id=message.chat.id, document=my_document)
    await message.reply("Ma'lumotlar uchun rahmat!!!")
    await state.finish()


@dp.message_handler(Text(equals='Tugatish', ignore_case=True))
async def exit_menu(message: types.Message):
    await message.answer("Sertifikatingiz tayyorlanmoqda biroz kuting...")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
