import datetime
import os


class Settings:
    def get_keywords(self) -> list[str]:
        """Для получения списка ключевых слов."""
        file_path = os.path.join(os.path.dirname(__file__), 'keywords.txt')
        with open(file_path, 'rt', encoding='utf-8') as f:
            return [k.strip() for k in f]

    def date_date(self) -> tuple[str, str]:
        """Для получения даты. Обычно сегодня и вчера."""
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        formatted_today = today.strftime("%d.%m.%Y")
        formatted_yesterday = yesterday.strftime("%d.%m.%Y")
        return (formatted_today, formatted_yesterday)



