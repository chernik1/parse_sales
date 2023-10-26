import datetime
import os

file_path = os.path.join(os.path.dirname(__file__), 'keywords_test')

def get_keywords() -> list[str]:
    with open(file_path, 'rt', encoding='utf-8') as f:
        return [k.strip() for k in f]

def date_date() -> tuple[str, str]:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    formatted_today = today.strftime("%d.%m.%Y")
    formatted_yesterday = yesterday.strftime("%d.%m.%Y")
    return (formatted_today, formatted_yesterday)

today, yesterday = date_date()
keywords = get_keywords()