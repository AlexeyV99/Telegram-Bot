import time
from database.sqlite_db_loader import user_history
from loguru import logger
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Dispatcher
from loader import dp, bot
from database.sqlite_db_loader import user_info


# def time_formate(t: float):
#     named_tuple = time.localtime(t)  # получить struct_time
#     time_string = time.strftime("%d.%m.%Y %H:%M", named_tuple)
#     return time_string


# Ответ на команду history
async def history(message: Message) -> None:
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "history"')
    user_history_list = user_history(message.from_user.id)
    if user_history_list:
        text = [f'{u_time}  {command}  {hotels}' for command, u_time, hotels in user_history_list]
        await bot.send_message(message.from_user.id,
                         f'<b><u>Твоя история запросов, {message.from_user.full_name}:</u></b>\n'+'\n'.join(text),
                         parse_mode='html', reply_markup=ReplyKeyboardRemove())
        logger.info(f"Пользователь {message.from_user.full_name}({message.from_user.id}) запросил свою историю поисков")
    else:
        await bot.send_message(message.from_user.id,
                         f'<b><u>{message.from_user.full_name}, твоя история запросов пуста!</u></b>',
                               parse_mode='html',
                               reply_markup=ReplyKeyboardRemove())


# Ответ на команду user_info
async def user_info_handler(message: Message) -> None:
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) запросил информацию о себе')
    info = user_info(message)
    text = '== ВАШИ ДАННЫЕ ==\nId пользователя: {0}\nИмя пользователя: {1}\nПрава: {2}\nЯзык: {3}'.format(
        info[0],
        info[1],
        info[2],
        info[3]
    )
    await bot.send_message(message.from_user.id, text, parse_mode='html', reply_markup=ReplyKeyboardRemove())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(user_info_handler, commands=['user_info'])
    dp.register_message_handler(history, commands=['history'])
