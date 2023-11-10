from .settings import combined_request
import g4f
from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
    AiAsk,
)

def run_ai(data):
    new_db_zaku = []

    for index, element in enumerate(data):
        print(element.price, element.main_name_purchase, element.location)
        promt = combined_request + element.location + ' , ' + element.main_name_purchase + ' , ' + element.price + "Напиши свой ответ без объяснений в виде **+** или **-** или **A**."
        # Set the provider
        print(promt)
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": promt}],
                stream=True,
            )
        except Exception as e:
            print(e)
            response = ['None']
        s = ''
        for i in response:
            s += i
        if '**+**' in s:
            forecast = 'Купить'
        elif '**-**' in s:
            forecast = 'Не купить'
        elif '**A**' in s:
            forecast = 'Не знаю'
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




