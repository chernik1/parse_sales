import datetime
import os


class Settings:
    def get_keywords(self) -> list[str]:
        file_path = os.path.join(os.path.dirname(__file__), 'keywords.txt')
        with open(file_path, 'rt', encoding='utf-8') as f:
            return [k.strip() for k in f]

    def date_date(self) -> tuple[str, str]:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=2)
        formatted_today = today.strftime("%d.%m.%Y")
        formatted_yesterday = yesterday.strftime("%d.%m.%Y")
        return (formatted_today, formatted_yesterday)



