import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_mod import reply_with_intent
from loggers import configure_logger


logger = logging.getLogger(__file__)


def start(update, context):
    update.message.reply_text("Здравствуйте! Чем можем помочь?")


def reply(update, context):
    try:
        message, _ = reply_with_intent(
            f"tg-{update.effective_chat.id}", update.message.text
        )
        update.message.reply_text(message)
    except Exception as err:
        logger.error(err)


def main():
    load_dotenv()
    configure_logger(logger)
    
    bot = Updater(os.environ["TELEGRAM_TOKEN"])

    bot.dispatcher.add_handler(CommandHandler("start", start))
    bot.dispatcher.add_handler(MessageHandler(Filters.text, reply))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
