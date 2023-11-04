# from .settings import combined_request
# import g4f
#
# def run_ai(data):
#     element = data[0]
#     request = str(combined_request) + element.location + element.main_name_purchase + element.price
#     # Set with provider
#     response = g4f.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": request}]
#     )
#     print(response)