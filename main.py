from loader import dp, bot
from aiogram.utils import executor
from aiogram.types import BotCommand
from handlers import default_handlers, user_handlers, lowprice
from loguru import logger
from config_data.config import DEFAULT_COMMANDS
import asyncio


async def setup_bot_commands(_) -> None:
    logger.info(f"Бот онлайн!")
    await bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])   # загрузка в бот команд по умолчанию


def main() -> None:
    user_handlers.register_user_handlers(dp)
    lowprice.register_lowprice_handlers(dp)
    default_handlers.register_default_handlers(dp)

    executor.start_polling(dp, skip_updates=False, on_startup=setup_bot_commands)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    # asyncio.run(main())
    main()
