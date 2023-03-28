from aiogram.utils import executor
from loader import dp, shutdown, log_func, setup_bot_commands
from handlers import default_handlers, user_handlers, lowprice


def main() -> None:
    log_func()
    user_handlers.register_user_handlers(dp)
    lowprice.register_lowprice_handlers(dp)
    default_handlers.register_default_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands, on_shutdown=shutdown)


if __name__ == '__main__':
    main()
