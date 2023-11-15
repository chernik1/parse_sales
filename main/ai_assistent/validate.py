
def is_furniture(string: str) -> bool:
    tuple_keywords = (
        'мебел', 'мебель', 'стул', 'кровать', 'кресло', 'кресла', 'матрас', 'шкаф', 'диван', 'тумба', 'стол', 'комод', 'полка', 'зеркало',
        'пуф', 'банкетка', 'табурет', 'кушетка', 'секретер', 'бюро', 'сундук', 'этажерка', 'вешалка',
        'подушка', 'одеяло', 'плед', 'скамья', 'лампа', 'ковер', 'подставка', 'сервант'
    )

    string = string.lower()

    return any(word in string for word in tuple_keywords)

def is_chemistry(string: str) -> bool:
    tuple_keywords = (
        'химия', 'реагент', 'молекул', 'атом', 'ион', 'валентност', 'формула', 'реакция',
        'катализатор', 'кислота', 'основание', 'соль', 'окислитель', 'восстановитель', 'раствор', 'концентрация',
        'осадок', 'газ', 'твердое', 'жидкое', 'коллоид', 'электролит', 'неэлектролит', 'показатель', 'краситель',
        'индикатор', 'титрование', 'анализ', 'синтез', 'деструкция', 'полимер', 'мономер', 'алкан', 'алкен', 'алкин',
        'аромат', 'функциональная группа', 'изомерия', 'стереохимия', 'химич'
    )

    string = string.lower()

    return any(word in string for word in tuple_keywords)
def is_validate(element):

    string = element.name_purchase

    check_furniture: bool = is_furniture(string)
    check_chemistry: bool = is_chemistry(string)

    return any((check_furniture, check_chemistry))



