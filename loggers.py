import logging
import os

from telegram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id
        self.tg_bot = Bot(self.token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def configure_logger(logger):
    logger.setLevel(logging.ERROR)
    handler = TelegramLogsHandler(
        os.environ["LOGGER_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
    )
    formatter = logging.Formatter("%(asctime)s: %(filename)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
