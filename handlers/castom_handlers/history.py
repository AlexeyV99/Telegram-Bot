from keyboards.reply.hotel_foto_yn import request_hotel_foto_yn
from loader import bot
from states.user_info import UserInfoState
from telebot.types import Message
from database.sqlite_db_loader import user_history


'''
UserInfoState:
    [user_country]      страна
    [user_city]         город
    [user_hotel_num]    кол-во отелей
    [user_foto]         фото
'''


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    user_history_list = user_history(message.from_user.id)
    text = [f'{country} - {city}' for country, city in user_history_list]
    bot.send_message(message.from_user.id,
                     f'<b><u>Твоя история запросов, {message.from_user.full_name}:</u></b>\n'+'\n'.join(text),
                     parse_mode='html')

    # bot.set_state(message.from_user.id, UserInfoState.user_country, message.chat.id)
    # bot.send_message(message.from_user.id, f'Введи название страны:')

# @bot.message_handler(state=UserInfoState.user_country)
# def get_country(message: Message) -> None:
#     bot.send_message(message.from_user.id, 'Теперь введи название города:')
#     bot.set_state(message.from_user.id, UserInfoState.user_city, message.chat.id)
#
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['user_country'] = message.text
#
# @bot.message_handler(state=UserInfoState.user_city)
# def get_city(message: Message) -> None:
#     bot.send_message(message.from_user.id, 'Теперь введи кол-во отелей для показа:')
#     bot.set_state(message.from_user.id, UserInfoState.user_hotel_num, message.chat.id)
#
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['user_city'] = message.text
#
# @bot.message_handler(state=UserInfoState.user_hotel_num)
# def get_hotel_num(message: Message) -> None:
#     if message.text.isdigit():
#         bot.send_message(message.from_user.id,
#                          'Теперь скажи, нужны ли фото?',
#                          reply_markup=request_hotel_foto_yn())
#         bot.set_state(message.from_user.id, UserInfoState.user_foto, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['user_hotel_num'] = int(message.text)
#     else:
#         bot.send_message(message.from_user.id, 'Неверный ввод кол-ва отелей!')
#
# @bot.message_handler(content_types=['text', 'hotel_foto_yn'], state=UserInfoState.user_foto)
# def get_foto(message: Message) -> None:
#     # if message.content_type == 'hotel_foto_yn':
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['user_foto'] = message.text
#         bot.send_message(message.from_user.id, '<b>Данные сохранены!</b>', parse_mode='html')
#         text = 'Страна: <b>{}</b>\nгород: <b>{}</b>\nКол-во отелей для показа: <b>{}</b>\nФото: <b>{}</b>'.format(
#             data['user_country'],
#             data['user_city'],
#             data['user_hotel_num'],
#             data['user_foto']
#         )
#         bot.send_message(message.from_user.id, text, parse_mode='html')
#         db_loader(message.from_user.id, data['user_country'], data['user_city'], data['user_hotel_num'], data['user_foto'])
#     bot.delete_state(message.from_user.id, message.chat.id)


