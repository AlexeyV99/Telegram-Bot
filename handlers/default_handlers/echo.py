from telebot.types import Message
from loader import bot
from handlers.default_handlers.help import bot_help


@bot.message_handler(state=None)
def bot_echo(message: Message):
    # Эхо хендлер, куда летят текстовые сообщения без указанного состояния
    bot.reply_to(message.from_user.id, f"Не плохо сказано, дружище.")
    bot_help(message)

