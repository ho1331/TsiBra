import os

import requests
import dialogflow
from bs4 import BeautifulSoup
from google.api_core.exceptions import InvalidArgument


# Enviroment
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
DIALOGFLOW_PROJECT_ID = 'small-talk-cktl'
DIALOGFLOW_LANGUAGE_CODE = 'ru'
SESSION_ID = 'me'


SIGN_RU = (
    'Овен',
    'Телец',
    'Близнецы',
    'Рак',
    'Лев',
    'Дева',
    'Весы',
    'Скорпион',
    'Стрелец',
    'Козерог',
    'Водолей',
    'Рыбы',
)
SIGN_US = (
    'Aries',
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn',
    'Aquarius',
    'Pisces'
)

SIGNS = dict(zip(SIGN_RU, SIGN_US))


def horoskop_parser(sign):
    url = f'https://www.elle.ru/astro/{SIGNS.get(sign).lower()}/day/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    alldiv = soup.find('div', class_='articleParagraph articleParagraph_dropCap')
    horoskop = alldiv.find('p').text

    return horoskop


def answer_by_ai(message):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    answer = "Упс, чет мне плохо..."
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        answer = response.query_result.fulfillment_text \
            if response.query_result.fulfillment_text \
            else "Я пока затрудняюсь ответить"

    except InvalidArgument:
        raise

    return answer
