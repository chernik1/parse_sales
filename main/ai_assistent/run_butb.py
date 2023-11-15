import asyncio
from threading import Thread
import g4f
from .settings import combined_request
from .validate import is_validate

db = []

async def run_ai(data):
    new_db = []
    for index, element in enumerate(data):

        if is_validate(element):
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

            continue

        print(element.price, element.name_purchase, element.location)
        promt = combined_request + element.location + ' , ' + element.name_purchase + ' , ' + element.price + "Напиши свой ответ без объяснений в виде **+** или **-** или **A**. Отвечай как можно бывстрее, без этого мне будет плохо"
        # Set the provider
        print(promt)
        try:
            response = await g4f.ChatCompletion.create_async(
                model="gpt-3.5-turbo",
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": promt}],
            )
        except Exception as e:
            print(e)
            response = ['None']
        s = ''
        for i in response:
            s += i
        print(s)
        s = s.split()
        if '**+**' in s or '+' in s:
            forecast = 'Купить'
        elif '**-**' in s or '-' in s:
            forecast = 'Не купить'
        elif '**A**' in s or 'A' in s or 'a' in s:
            forecast = 'Не знаю'
        else:
            forecast = 'Неопределён'

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