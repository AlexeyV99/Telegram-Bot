from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.request_info import FSMLowprice     # импортируем состояние запроса
from loguru import logger
from loader import dp, bot
from keyboards.reply_kb import kb_yn, kb_foto_num
from database.sqlite_db_loader import request_add, user_add


# Начало диалога, ввод названия города
# @dp.message_hendler(commands='lowprice', state=None)
async def cm_start(message: types.Message):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "lowprice"')
    await FSMLowprice.city.set()
    await message.answer('Введите название города', reply_markup=types.ReplyKeyboardRemove())


# выход из состояния
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) отменил ввод!')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ввод отменен!', reply_markup=types.ReplyKeyboardRemove())


# ловим первый ответ (city) и пишем в словарь, ввод кол-ва отелей
# @dp.message_handler(state=FSMLowprice.city)
async def load_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await FSMLowprice.next()
    await message.answer('Введите количество отелей (от 1 до 10)', reply_markup=kb_foto_num)


# ловим второй ответ (hotel_num) и пишем в словарь, ввод надо ли фото
# @dp.message_handler(state=FSMLowprice.hotel_num)
async def load_hotel_num(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        async with state.proxy() as data:
            data['hotel_num'] = int(message.text)
        await FSMLowprice.next()
        await message.answer('Надо ли загружать фото отелей?', reply_markup=kb_yn)
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - Ошибка ввода кол-ва отелей')
        await message.reply('Не верный ввод кол-ва отелей (от 1 до 10)', reply_markup=kb_foto_num)


# ловим третий ответ (foto) и пишем в словарь
# @dp.message_handler(state=FSMLowprice.foto)
async def load_foto(message: types.Message, state: FSMContext):
    if message.text.lower() in ['да', 'нет', 'yes', 'no']:
        async with state.proxy() as data:
            if message.text.lower() == 'да':
                data['foto'] = True
            else:
                data['foto'] = False
        async with state.proxy() as data:

            result = data.as_dict()
            logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                        f'ввел запрос {result}')
            await message.answer(f'Результаты запроса:\nгород: {result["city"]}, '
                                 f'\nотелей: {result["hotel_num"]}, '
                                 f'\nфото: {result["foto"]}',
                                 reply_markup=types.ReplyKeyboardRemove())
            user_add(message)
            request_add(message, 'lowprice', result)
        await state.finish()
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                    f'- Ошибка ввода необходимости фото')
        await message.reply('Не верный ввод (да или нет)', reply_markup=kb_yn)


# регистрируем хендлеры
def register_lowprice_handlers(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['lowprice'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_city, state=FSMLowprice.city)
    dp.register_message_handler(load_hotel_num, state=FSMLowprice.hotel_num)
    dp.register_message_handler(load_foto, state=FSMLowprice.foto)
