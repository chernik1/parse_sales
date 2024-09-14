from asyncio import create_task

import g4f
from attr.setters import validate
from ..models import ParserZaku

from .settings import combined_request
from .validate import is_validate
import re

db = []

def make_request(prompt):
    """Функция для выполнения запроса."""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        print(e)
        response = ['None']
    return response

def get_responses(data):
    responses = []

    for i, el in enumerate(data, 0):
        prompt = combined_request + el.main_name_purchase
        response = make_request(prompt)
        responses.append(response)

    return responses

def run_ai(data):
    new_db_zaku = []
    validate_data = []

    for index, element in enumerate(data):
        if not is_validate(element):
            new_db_zaku.append(
                {
                    'keyword': element.keyword,
                    'url': element.url,
                    'name_company': element.name_company,
                    'payer_number': element.payer_number,
                    'main_name_purchase': element.main_name_purchase,
                    'name_purchase': element.name_purchase,
                    'price': element.price,
                    'location': element.location,
                    'forecast': 'Проверка не пройдена',
                }
            )
        else:
            validate_data.append(element)

        all_responses = get_responses(validate_data)

        for index, response in enumerate(all_responses):
            element = data[index]
            s = ''
            for i in response:
                s += i

            pattern_buy = r"\*\*\+\*\*"
            pattern_not_buy = r"\*\*\-\*\*"
            pattern_unknown = r"\*\*\A\*\*"

            if re.search(pattern_buy, s):
                forecast = 'Купить'
            elif re.search(pattern_not_buy, s):
                forecast = 'Не купить'
            elif re.search(pattern_unknown, s):
                forecast = 'Не знаю'
            else:
                forecast = 'Неопределён'
            print(s)

            new_db_zaku.append(
                {
                    'keyword': element.keyword,
                    'url': element.url,
                    'name_company': element.name_company,
                    'payer_number': element.payer_number,
                    'main_name_purchase': element.main_name_purchase,
                    'name_purchase': element.name_purchase,
                    'price': element.price,
                    'location': element.location,
                    'forecast': forecast,
                }
            )

        return new_db_zaku

def run_programm(db_zaku):
    return run_ai(db_zaku)

if __name__ == '__main__':
    data = ParserZaku.objects.all()
    print(run_programm(data))