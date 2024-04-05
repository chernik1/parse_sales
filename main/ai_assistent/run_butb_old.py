import asyncio
from threading import Thread
import g4f
from .settings import combined_request
from .validate import is_validate
import re

db = []

async def make_request(prompt):
    """Функция для выполнения запроса."""
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": prompt}],
    )

    return response

async def create_tasks(data, new_db):
    """Функция для создания задач."""
    tasks = []

    for index, element in enumerate(data):
        print(element.price, element.name_purchase, element.location)
        prompt = combined_request + element.name_purchase

        if not is_validate(element):
            new_db.append(
                {
                    'keyword': element.keyword,
                    'id_purchase': element.id_purchase,
                    'name_company': element.name_company,
                    'payer_number': element.payer_number,
                    'date': element.date,
                    'name_purchase': element.name_purchase,
                    'price': element.price,
                    'location': element.location,
                    'forecast': 'Проверка не пройдена',
                }
            )

        print(prompt)
        task = asyncio.create_task(make_request(prompt))
        tasks.append(task)

    return tasks, new_db


async def run_ai(data):
    """Функция работы AI."""
    new_db_butb = []
    all_responses = []

    data_50_split = [data[i:i+10] for i in range(0, len(data), 10)]

    for data_50 in data_50_split:
        tasks, new_db_zaku = await create_tasks(data_50, new_db_butb)
        responses = await asyncio.gather(*tasks)
        all_responses.append(responses)

    all_responses = [item for sublist in all_responses for item in sublist]

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

        new_db_butb.append(
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

    return new_db_butb


def run_programm(data):
    """Функция запуска AI."""
    global db

    def run_async_code():
        global db
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_ai(data))
        loop.close()
        db = result
        return result

    thread = Thread(target=run_async_code)
    thread.start()
    thread.join()

    return db