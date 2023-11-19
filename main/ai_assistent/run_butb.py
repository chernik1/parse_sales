import asyncio
from threading import Thread
import g4f
from .settings import combined_request
from .validate import is_validate

db = []

async def create_tasks(data, new_db):
    tasks = []

    for index, element in enumerate(data):
        print(element.price, element.name_purchase, element.location)
        promt = combined_request + element.name_purchase

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

        print(promt)
        task = asyncio.create_task(make_request(promt))
        tasks.append(task)

    return tasks, new_db

async def make_request(promt):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": promt}],
        )
    except Exception as e:
        print(e)
        response = ['None']
    return response

async def run_ai(data):
    new_db = []

    tasks, new_db = await create_tasks(data, new_db)

    responses = await asyncio.gather(*tasks)

    for index, response in enumerate(responses):
        element = data[index]
        s = ''
        for i in response:
            s += i
        s = s.split()
        if '**+**' in s or '+' in s:
            forecast = 'Купить'
        elif '**-**' in s or '-' in s:
            forecast = 'Не купить'
        elif '**A**' in s or 'A' in s:
            forecast = 'Не знаю'
        else:
            forecast = 'Неопределён'
        print(s)

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
                'forecast': forecast,
            }
        )

    return new_db


def run_programm(data):
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