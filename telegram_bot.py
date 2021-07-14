import logging
import os

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from utils import reply_with_intent


def start(update, context):
    update.message.reply_text("Здравствуйте! Чем можем помочь?")


def reply(update, context):
    message = reply_with_intent(update.effective_chat.id, update.message.text)
    update.message.reply_text(message)


if __name__ == "__main__":
    logging.basicConfig(
        filename="bot.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    bot = Updater(os.environ["TELEGRAM_TOKEN"])

    bot.dispatcher.add_handler(CommandHandler("start", start))
    bot.dispatcher.add_handler(MessageHandler(Filters.text, reply))

    bot.start_polling()
    bot.idle()
