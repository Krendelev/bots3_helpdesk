import logging
import random
import os

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from utils import reply_with_intent, TelegramLogsHandler

logger = logging.getLogger(__file__)


def reply(event, vk_api):
    message, fallback = reply_with_intent(event.user_id, event.text)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id, message=message, random_id=random.getrandbits(32)
        )


def main():
    logger.setLevel(logging.ERROR)
    handler = TelegramLogsHandler(
        os.environ["LOGGER_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
    )
    logger.addHandler(handler)

    vk_session = vk.VkApi(token=os.getenv("VK_ACCESS_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api)
    except Exception as err:
        logger.error(err)


if __name__ == "__main__":
    main()