from .settings import combined_request
import g4f

def run_ai(data):
    for i in range(4, 15):
        element = data[i]
        print(element.price, element.main_name_purchase, element.location)
        request = str(combined_request) + element.location + element.main_name_purchase + element.price + 'Твой ответ только + или -(без пояснений)'
        # Set the provider
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request}],
            provider=g4f.Provider.FreeGpt,
            stream=True,
        )
        for chunk in response:
            print(chunk)

