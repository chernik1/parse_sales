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
        request = combined_request + element.location + ' + ' + element.main_name_purchase + ' + ' + element.price + 'Ответ 1 символ + или -'
        # Set the provider
        print(request)
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": request}],
                provider=g4f.Provider.ChatgptAi,
                stream=True,
            )
        except Exception as e:
            response = ['None']
        s = ''
        for i in response:
            s += i
        print(s)


