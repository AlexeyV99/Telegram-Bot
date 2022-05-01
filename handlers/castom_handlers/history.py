from keyboards.reply.hotel_foto_yn import request_hotel_foto_yn
from states.user_info import UserInfoState
from telebot.types import Message
from database.sqlite_db_loader import user_history
from loader import bot
import time



def time_formate(t: float):
    named_tuple = time.localtime(t)  # получить struct_time
    time_string = time.strftime("%d.%m.%Y %H:%M", named_tuple)
    return time_string


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    user_history_list = user_history(message.from_user.id)
    if user_history_list:
        text = [f'{time_formate(float(u_time))}  {command}  {hotels}' for command, u_time, hotels in user_history_list]
        bot.send_message(message.from_user.id,
                         f'<b><u>Твоя история запросов, {message.from_user.full_name}:</u></b>\n'+'\n'.join(text),
                         parse_mode='html')
    else:
        bot.send_message(message.from_user.id,
                         f'<b><u>{message.from_user.full_name}, твоя история запросов пуста!</u></b>', parse_mode='html')
