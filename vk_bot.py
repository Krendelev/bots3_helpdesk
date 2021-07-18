import logging
import random
import os

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_mod import reply_with_intent
from loggers import configure_logger

logger = logging.getLogger(__file__)


def reply(event, vk_api):
    message, fallback = reply_with_intent(f"vk-{event.user_id}", event.text)
    if not fallback:
        vk_api.messages.send(
            user_id=event.user_id, message=message, random_id=random.getrandbits(32)
        )


def main():
    load_dotenv()
    configure_logger(logger)

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
