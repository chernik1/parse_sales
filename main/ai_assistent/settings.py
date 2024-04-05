from main.parsers.settings import Settings

keywords = Settings.get_keywords(self=Settings)

BASE_REQUEST = ("""Тебе поданы данны ввиде место закупки-краткое описание предмета-полное описание предмета-цена за всё.
                 Тебе нужно к каждому предмету справа написать подходит ли товар пол следущие критерии.  Для
                 обозначения испротзуй + если стоит купить и - если не стоит купить.""")

CRITERIA_REQUEST = f"""То что находится в Минске или Минской области интересует цена от 2 тысячи рублей. Остальные регионы от 3 тысяч рубелй.
                      Всё в беларусских рублях. Интересует только компьютерная техника, различные приборы, системные блоки, пвэм и персональная компьютерная техника, закупки компьютеров, вычислительная техника и так далее. Я компания, которая хочет выкупить всю технику электронную для компьютеров, также телефоны и принтеры и планшеты. .Вот твоё задание. Напиши только 1 символ + или -. -> """

# combined_request = BASE_REQUEST + ' ' + CRITERIA_REQUEST
combined_request = 'Определи является ли товар подходящим под 1 из критериев: это ноутбук, это компьютер, это ПЭВМ, это ЭВМ, это принтер, это телефон, это планшет, это моноблок. Предмет не должен быть связан с медециной. Твой ответ должен быть либо **+** если подходит, либо **-** если не подходит. Вот его название.'

SYSTEM_PROMT = 'You will be given 3 data separated by commas, the first is the name, the second is the price and then this name. You need to classify whether this product can be bought or not according to the following criteria. An item can be purchased if it is a piece of computer equipment (various computer components, laptops and all other electronics). An item cannot be purchased if it is part of furniture, rugs or other unnecessary goods. The price should be over 1000 for the Minsk city location. And over 1500 for another location. Your answer for or not is just words without different symbols.'