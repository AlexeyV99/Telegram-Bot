from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.request_info import FSMLowprice     # импортируем состояние запроса
from loguru import logger
from loader import dp, bot
from keyboards.reply_kb import kb_yn, kb_foto_num, kb_generator
from database.sqlite_db_loader import request_add, user_add
from req_json import search_city, search_hotel
from keyboards.inline_kb import kb_cities


# Начало диалога, ввод названия города
@dp.callback_query_handler(text='/lowprice')
@dp.message_handler(commands=['lowprice'], state=None)
async def cm_start(message: types.Message):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "lowprice"')
    await FSMLowprice.city_dict.set()
    await message.answer('Введите название города')


# выход из состояния
async def cancel_handler(message: types.Message, state: FSMContext):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) отменил ввод!')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ввод отменен!', reply_markup=types.ReplyKeyboardRemove())


async def load_dif_city(message: types.Message, state: FSMContext):
    """
    выбираем ответ ответ (city) и пишем в словарь
    :param message:
    :param state:
    :return:
    """
    rezult = search_city.s_city(message.text)
    if rezult:
        async with state.proxy() as data:
            data['city_dict'] = rezult

        await message.answer('Уточните метоположение', reply_markup=kb_cities(rezult))
        await FSMLowprice.next()
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - Ошибка ввода названия города')


async def load_city(callback: types.CallbackQuery, state: FSMContext):
    """
    ловим первый ответ (city) и пишем в словарь, ввод кол-ва отелей
    :param callback:
    :param state:
    :return:
    """
    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        data['city'] = callback.data
    await FSMLowprice.next()
    await callback.message.answer('Введите количество отелей (от 1 до 10)', reply_markup=kb_foto_num)


# ловим второй ответ (hotel_num) и пишем в словарь, ввод надо ли фото
async def load_hotel_num(message: types.Message, state: FSMContext):
    """
    ловим второй ответ (hotel_num) и пишем в словарь, ввод надо ли фото
    :param message:
    :param state:
    :return:
    """
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        async with state.proxy() as data:
            data['hotel_num'] = int(message.text)
        await FSMLowprice.next()
        await message.answer('Надо ли загружать фото отелей?', reply_markup=kb_yn)
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - Ошибка ввода кол-ва отелей')
        await message.reply('Не верный ввод кол-ва отелей (от 1 до 10)', reply_markup=kb_foto_num)


async def load_foto(message: types.Message, state: FSMContext):
    """
    ловим третий ответ (foto) и пишем в словарь
    :param message:
    :param state:
    :return:
    """
    if message.text.lower() in ['да', 'нет', 'yes', 'no']:
        async with state.proxy() as data:
            if message.text.lower() == 'да':
                data['foto'] = True
            else:
                data['foto'] = False
        async with state.proxy() as data:

            result = data.as_dict()
            logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) ввел запрос lowprice')
            await message.answer(f'Результаты запроса:\nгород: {result["city"]} - {result["city_dict"][result["city"]]},'
                                 f'\nотелей: {result["hotel_num"]}, '
                                 f'\nфото: {result["foto"]}'
                                 f'\nЗапрос обрататывается...',
                                 reply_markup=types.ReplyKeyboardRemove())

            # all_hotel = search_hotel.s_hotel(result["city_dict"][result["city"]], int(result["hotel_num"]), int(result["foto"]))
            all_hotel = search_hotel.s_hotel(result["city"])
            if not all_hotel:
                await message.answer('Ошибка поиска отелей')
            else:
                print(all_hotel)
            # print(all_hotel)
            # for i_name, i_value in all_hotel.items():
            #     hotel_text = f'{i_name}\n{i_value["address"]}\n{i_value["price"]}{i_value["hotel_foto"]}\n' \
            #                  f'{i_value["link"]}'
            #     await message.answer(hotel_text)
            # user_add(message)
            # request_add(message, 'lowprice', result)
        await state.finish()
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                    f'- Ошибка ввода необходимости фото')
        await message.reply('Не верный ввод (да или нет)', reply_markup=kb_yn)


# регистрируем хендлеры
def register_lowprice_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_dif_city, state=FSMLowprice.city_dict)
    # dp.register_message_handler(load_city, state=FSMLowprice.city)
    dp.register_callback_query_handler(load_city, state=FSMLowprice.city)
    dp.register_message_handler(load_hotel_num, state=FSMLowprice.hotel_num)
    dp.register_message_handler(load_foto, state=FSMLowprice.foto)

