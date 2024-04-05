import asyncio
import replicate
from threading import Thread
from .settings import SYSTEM_PROMT
from .validate import is_validate
import re

db = []

async def run_model(prompt, system_prompt):
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": prompt,
            "system_prompt": system_prompt,
        }
    )

    loop = asyncio.get_running_loop()
    iterator = await loop.run_in_executor(None, lambda: iter(output))
    answer = ''
    for item in iterator:
        answer += item
    return answer

async def run_ai(data):
    """Функция работы AI."""
    new_db_zaku = []
    all_responses = []

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

    tasks = []

    for element in validate_data:
        prompt = ','.join([element.main_name_purchase, element.price, element.location])
        task = asyncio.create_task(run_model(prompt, SYSTEM_PROMT))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    for response in responses:
        if re.search(r'Not', response, re.IGNORECASE):
            forecast = 'Не купить'
        elif re.search(r'Buy', response, re.IGNORECASE):
            forecast = 'Купить'
        elif re.search(r'Yes', response, re.IGNORECASE):
            forecast = 'Купить'
        else:
            forecast = 'Неопределён'

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