import json
import logging
import os

from google.cloud import dialogflow
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


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    handler = TelegramLogsHandler(
        os.environ["LOGGER_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
    )
    formatter = logging.Formatter("%(asctime)s: %(filename)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def load_json(filepath):
    with open(filepath) as fh:
        return json.load(fh)


# modified from https://cloud.google.com/dialogflow/es/docs/quick/api
def reply_with_intent(session_id, text, language_code="ru"):
    creds = load_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(creds["project_id"], session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return (
        response.query_result.fulfillment_text,
        response.query_result.intent.is_fallback,
    )


# modified from https://cloud.google.com/dialogflow/es/docs/how/manage-intents#create-intent-python
def create_intent(display_name, training_phrases_parts, message_texts):
    creds = load_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(creds["project_id"])
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print(f"Intent created: {response.display_name}")


if __name__ == "__main__":
    intents = load_json("training_phrases.json")

    for intent in intents:
        create_intent(
            intent,
            intents[intent]["questions"],
            [intents[intent]["answer"]],
        )
