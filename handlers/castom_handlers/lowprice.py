from keyboards.reply.hotel_foto_yn import request_hotel_foto_yn
from loader import bot
from states.user_info import UserInfoState
from telebot.types import Message

'''
UserInfoState:
    [user_country]      страна
    [user_city]         город
    [user_hotel_num]    кол-во отелей
    [user_foto]         фото
'''


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.user_country, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название страны:')


@bot.message_handler(stat=UserInfoState.user_country)
def get_country(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Теперь введите название города:')
    bot.set_state(message.from_user.id, UserInfoState.user_city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_country'] = message.text

@bot.message_handler(stat=UserInfoState.user_city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Теперь введите кол-во отелей для показа:')
    bot.set_state(message.from_user.id, UserInfoState.user_hotel_num, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_city'] = message.text

@bot.message_handler(stat=UserInfoState.user_hotel_num)
def get_hotel_num(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id,
                         'Теперь скажи, нужны ли фото?',
                         reply_markup=request_hotel_foto_yn())
        bot.set_state(message.from_user.id, UserInfoState.user_foto, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['user_hotel_num'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Неверный ввод кол-ва отелей!')

@bot.message_handler(stat=UserInfoState.user_foto)
def get_foto(message: Message) -> None:
    # if message.content_type == 'hotel_foto_yn':
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_foto'] = message.text
        bot.send_message(message.from_user.id, 'Данные сохранены!')
        print(data)
    # else:
    #     bot.send_message(message.from_user.id, 'Ошибка!')
