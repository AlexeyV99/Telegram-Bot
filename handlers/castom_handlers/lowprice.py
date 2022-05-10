from loguru import logger
from keyboards.reply.hotel_foto_yn import request_hotel_foto_yn
from keyboards.inline.inline_kb import inline_keyboard_yn
from loader import bot
from states.user_info import UserInfoState
from telebot.types import Message
from database.sqlite_db_loader import request_add, user_add


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.user_city, message.chat.id)
    bot.send_message(message.from_user.id, f'Введи название города:')


@bot.message_handler(state=UserInfoState.user_city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Теперь введи кол-во отелей для показа (от 1 до 10):')
    bot.set_state(message.from_user.id, UserInfoState.user_hotel_num, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_city'] = message.text


@bot.message_handler(state=UserInfoState.user_hotel_num)
def get_hotel_num(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= 10:
        bot.send_message(message.from_user.id,
                         'Теперь скажи, нужны ли фото?',
                         reply_markup=inline_keyboard_yn())
        bot.set_state(message.from_user.id, UserInfoState.user_foto, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['user_hotel_num'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Неверный ввод кол-ва отелей!\nНеобходимо ввести число от 1 до 10')
        logger.info('Ошибка ввода показа кол-ва отелей. ')


@bot.message_handler(content_types=['text', 'hotel_foto_yn'], state=UserInfoState.user_foto)
def get_foto(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_foto'] = message.text
        bot.send_message(message.from_user.id, '<b>Данные сохранены!</b>', parse_mode='html')
        text = 'Город: <b>{}</b>\nКол-во отелей для показа: <b>{}</b>\nФото: <b>{}</b>'.format(
            data['user_city'],
            data['user_hotel_num'],
            data['user_foto']
        )
        bot.send_message(message.from_user.id, text, parse_mode='html')
        # request_add(int(message.from_user.id), data['user_city'], data['user_hotel_num'], data['user_foto'])
        request_add(int(message.from_user.id))
        user_add(message)
    bot.delete_state(message.from_user.id, message.chat.id)

    # else:
    #     bot.send_message(message.from_user.id, 'Ошибка ввода!')
