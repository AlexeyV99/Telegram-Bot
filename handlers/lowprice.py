from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.request_info import FSMLowprice                     # импортируем состояние запроса
from loguru import logger
from loader import bot
from keyboards.reply_kb import kb_yn, kb_foto_num, kb_reply_cancel
from database.sqlite_db_loader import request_add, user_add
from req_json import search_city, search_hotel
from keyboards.inline_kb import kb_cities, inline_keyboard_link, inline_keyboard_default


async def show_hotel_info(chat_id, i_value: dict) -> None:
    """
    Пишет в чат информацию об отеле
    :param chat_id:
    :param i_value:
    :return:
    """
    text = f'Отель: {i_value["name"]}\nАдрес: {i_value["address"]}\nЦена: {i_value["f_price"]}'
    await bot.send_photo(chat_id=chat_id, photo=i_value['hotel_foto'][0], caption=text,
                         reply_markup=inline_keyboard_link(i_value['link']))


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Выход из машины состояний (FSM)
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) отменил ввод!')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ввод отменен!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Команды бота:', reply_markup=inline_keyboard_default())


async def cm_start(message: types.Message):
    """
    Начало диалога, точка входа. Ввод названия города
    :param message:
    :return:
    """
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "lowprice"')
    await bot.send_message(message.from_user.id, 'Введите название города', reply_markup=kb_reply_cancel)
    await FSMLowprice.city_dict.set()


async def load_dif_city(message: types.Message, state: FSMContext):
    """
    выбираем ответ ответ (city) и пишем в словарь
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Пользователь в функции load_dif_city!')
    rezult = search_city.search_city(message.text)
    if rezult:
        async with state.proxy() as data:
            data['city_dict'] = rezult

        await bot.send_message(message.from_user.id, 'Уточните метоположение', reply_markup=kb_cities(rezult))
        await FSMLowprice.next()
    else:
        logger.error(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - Ошибка ввода названия города')


async def load_city(callback: types.CallbackQuery, state: FSMContext):
    """
    ловим первый ответ (city) и пишем в словарь, ввод кол-ва отелей
    :param callback:
    :param state:
    :return:
    """
    logger.info(f'Пользователь в функции load_city!')

    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        data['city'] = callback.data
    await FSMLowprice.next()
    await callback.message.answer('Введите количество отелей (от 1 до 10)', reply_markup=kb_foto_num)


async def load_hotel_num(message: types.Message, state: FSMContext):
    """
    ловим второй ответ (hotel_num) и пишем в словарь, ввод - надо ли фото
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Пользователь в функции load_hotel_num!')

    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        async with state.proxy() as data:
            data['hotel_num'] = int(message.text)
        await FSMLowprice.next()
        await bot.send_message(message.from_user.id, 'Надо ли загружать фото отелей?', reply_markup=kb_yn)
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
    logger.info(f'Пользователь в функции load_foto!')

    if message.text.lower() in ['да', 'нет', 'yes', 'no']:
        async with state.proxy() as data:
            if message.text.lower() == 'да':
                data['foto'] = True
            else:
                data['foto'] = False
            logger.info(f'Пользователь ({message.from_user.id}) {data["city_dict"][data["city"]]} ({data["city"]}), '
                        f'lowprice, {data["hotel_num"]}')
            await bot.send_message(message.from_user.id, f'Запрос обрататывается...',
                                   reply_markup=types.ReplyKeyboardRemove())

            all_hotel = search_hotel.s_hotel(data["city"], data["hotel_num"])
            if not all_hotel:
                await message.answer('Ошибка поиска отелей')
            for i_value in all_hotel.values():
                await show_hotel_info(message.from_user.id, i_value)
            user_add(message)
            result = dict()
            result['hotels'] = all_hotel
            result['hotel_num'] = len(all_hotel)
            result['city'] = data["city_dict"][data["city"]]
            result['city_id'] = data["city"]
            request_add(message, 'lowprice', result)
        await state.finish()
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                    f'- Ошибка ввода необходимости фото')
        await message.reply('Не верный ввод (да или нет)', reply_markup=kb_yn)


def register_lowprice_handlers(disp: Dispatcher):
    """
    регистрируем хэндлеры
    :param disp:
    :return:
    """
    disp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    disp.register_callback_query_handler(cm_start, text='/lowprice')
    disp.register_message_handler(cm_start, commands=['lowprice'])
    disp.register_message_handler(load_dif_city, state=FSMLowprice.city_dict)
    disp.register_callback_query_handler(load_city, state=FSMLowprice.city)
    disp.register_message_handler(load_hotel_num, state=FSMLowprice.hotel_num)
    disp.register_message_handler(load_foto, state=FSMLowprice.foto)

