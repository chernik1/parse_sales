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
    for index, element in enumerate(data):
        print(element.price, element.main_name_purchase, element.location)
        request = combined_request + element.location + ' , ' + element.main_name_purchase + ' , ' + element.price + "Напиши свой ответ без объяснений в виде **+** или **-** или **A**."
        # Set the provider
        print(request)
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": request}],
                stream=True,
            )
        except Exception as e:
            print(e)
            response = ['None']
        s = ''
        for i in response:
            s += i
        if '**+**' in s:
            print('+')
        elif '**-**' in s:
            print('-')
        elif '**A**' in s:
            print('A')
        else:
            print(s)




