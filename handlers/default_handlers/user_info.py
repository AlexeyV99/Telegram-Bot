from telebot.types import Message
from loader import bot
from database.sqlite_db_loader import user_info
from handlers.default_handlers.help import bot_help


@bot.message_handler(commands=['user_info'])
def us_info(message: Message) -> None:
    info = user_info(message)
    text = '== ВАШИ ДАННЫЕ ==\nId пользователя: {0}\nИмя пользователя: {1}\nПрава: {2}\nЯзык: {3}'.format(
        info[0],
        info[1],
        info[2],
        info[3]
    )
    bot.send_message(message.from_user.id, text, parse_mode='html')
    bot_help(message)
