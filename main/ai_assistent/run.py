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
)

def run_ai(data):
    for i in range(4, 15):
        element = data[i]
        print(element.price, element.main_name_purchase, element.location)
        request = combined_request + element.location + ' , ' + element.main_name_purchase + ' , ' + element.price
        # Set the provider
        print(request)
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": request}],
                provider=g4f.Provider.Bing,
                stream=True,
                temperature=0.8,
            )
        except Exception as e:
            response = ['None']
        s = ''
        for i in response:
            s += i

        if '+' in s:
            print('Купить')
        elif '-' in s:
            print('Не купить')
        elif 'None' in s:
            print('None')
        else:
            print('A')


