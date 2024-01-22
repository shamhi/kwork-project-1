from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app.config import Config
from app.routers import user
from app.utils import logger
from app.middleware import InfoLoggerMiddleware, ConnectDB



async def aiogram_on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dp=dispatcher, bot=bot)
    dispatcher['aiogram_logger'].info("Started polling")


async def aiogram_on_shutdown(dispatcher: Dispatcher, bot: Bot):
    dispatcher['aiogram_logger'].debug("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher['aiogram_logger'].info("Stopped polling")


async def setup_aiogram(dp: Dispatcher, bot: Bot):
    await setup_commands(bot=bot)
    setup_logging(dp=dp)
    logger = dp['aiogram_logger']
    logger.debug("Configure aiogram")
    setup_i18n(dp=dp)
    setup_routers(dp=dp)
    setup_middleware(dp=dp)
    logger.info("Configured aiogram")


def setup_logging(dp: Dispatcher):
    dp['aiogram_logger'] = logger.bind(type='aiogram')
    dp['info_logger'] = logger.bind(type='info')


def setup_middleware(dp: Dispatcher):
    dp.update.outer_middleware(InfoLoggerMiddleware(dp['info_logger']))
    dp.message.middleware(ConnectDB('cargo'))


def setup_routers(dp: Dispatcher):
    dp.include_router(user)


async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Запуск'),
    ]

    await bot.set_my_commands(commands=commands)


def setup_i18n(dp: Dispatcher):
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path='app/locales/{locale}/LC_MESSAGES'
        ),
        default_locale='ru'
    )

    i18n_middleware.setup(dispatcher=dp)


def main():
    bot = Bot(token=Config.TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    dp.startup.register(aiogram_on_startup)
    dp.shutdown.register(aiogram_on_shutdown)

    dp.run_polling(bot)


if __name__ == '__main__':
    main()
