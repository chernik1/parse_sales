from playwright.async_api import async_playwright, Playwright, Page
import sys
import main.parsers.settings as settings
from bs4 import BeautifulSoup
from pprint import pprint
import asyncio
from threading import Thread
from main.models import ParserDelete

today, yesterday = settings.Settings().date_date()
keywords = settings.Settings().get_keywords()

id_purchase_list = []

list_of_keywords = []

async def check_page(page: Page) -> tuple[Page, list]:
    """Функция проверяет страницу на наличие товаров."""
    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    a_href_page_find = soup.find(class_="ui-datatable-data ui-widget-content")
    if a_href_page_find is None:
        return (page, [])
    a_href_page_find = a_href_page_find.find_all('a')

    if len(a_href_page_find) == 20:
        element_id = a_href_page_find[19]['id'].replace(':', '\\:').replace('\u0000', '')
        await page.wait_for_selector(f'#{element_id}', state='detached')

        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        tdoby_page_find = soup.find(class_="ui-datatable-data ui-widget-content")
        if tdoby_page_find is None:
            return (page, [])

        a_href_page_find = tdoby_page_find.find_all('a')
        tr_find_all = tdoby_page_find.find_all('tr')

        new_a_href_page_find = []

        for tr, a in zip(tr_find_all, a_href_page_find):

            if str(tr.find_all('td')[0].text.split()[0].replace('-', '')) in id_purchase_list:
                continue
            new_a_href_page_find.append(a)

        return (page, new_a_href_page_find)

    return (page, [])

async def parse_a_href(page: Page) -> tuple[Page, list]:
    """Функция для парсинга ссылок на страницы."""
    async def index_span(elements, keyword):
        index = 0
        if keyword in ('Полное наименование', 'УНП'):
            elements = elements[23:]
            index = 23
        for element in elements:
            if element.text == keyword:
                break
            index += 1
        return index

    list_of_objects = []

    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')

    register = soup(text='Регистрационный номер')
    register_tr = register[0].find_parent('div')
    register_all_span = register_tr.find_all('span')
    register_index = await index_span(register_all_span, 'Регистрационный номер')
    register_text = register_all_span[register_index + 1].text
    list_of_objects.append(register_text)

    name_company = soup(text='Полное наименование')
    name_company_tr = name_company[1].find_parent('div')
    name_company_all_span = name_company_tr.find_all('span')
    name_company_index = await index_span(name_company_all_span, 'Полное наименование')
    name_company_text = name_company_all_span[name_company_index + 1].text
    list_of_objects.append(name_company_text)

    date = soup(text='Дата размещения приглашения')
    date_tr = date[0].find_parent('div')
    date_all_span = date_tr.find_all('span')
    date_index = await index_span(date_all_span, 'Дата размещения приглашения')
    date_text = date_all_span[date_index + 1].text
    list_of_objects.append(date_text)

    name_purchase = soup(text='Наименование закупки')
    name_purchase_tr = name_purchase[0].find_parent('div')
    name_purchase_all_span = name_purchase_tr.find_all('span')
    name_purchase_index = await index_span(name_purchase_all_span, 'Наименование закупки')
    name_purchase_text = name_purchase_all_span[name_purchase_index + 1].text
    list_of_objects.append(name_purchase_text)

    price = soup(text='Предельная cтоимость закупки')
    text_price = 'Предельная cтоимость закупки'
    if len(price) == 0:
        price = soup(text='Ориентировочная cтоимость закупки')
        text_price = 'Ориентировочная cтоимость закупки'
    price_tr = price[0].find_parent('div')
    price_all_span = price_tr.find_all('span')
    price_index = await index_span(price_all_span, text_price)
    price_text = price_all_span[price_index + 1].text
    price_text = price_text.replace("\xa0", "").replace("\\xa", "")
    list_of_objects.append(price_text)

    payer_account_num = soup(text='УНП')
    payer_account_num_tr = payer_account_num[1].find_parent('div')
    payer_account_num_all_span = payer_account_num_tr.find_all('span')
    payer_account_num_index = await index_span(payer_account_num_all_span, 'УНП')
    payer_account_num_text = payer_account_num_all_span[payer_account_num_index + 1].text
    list_of_objects.append(payer_account_num_text)

    location = soup(text='Место нахождения')
    location_tr = location[0].find_parent('div')
    location_all_span = location_tr.find_all('span')
    location_index = await index_span(location_all_span, 'Место нахождения')
    location_text = location_all_span[location_index].text
    list_of_objects.append(location_text)

    return (page, list_of_objects)



async def step(page: Page, keyword: str) -> Page:
    """Функция перехода на страницу предметов."""
    await page.goto("https://zakupki.butb.by/auctions/reestrauctions.html")
    await page.get_by_role("link", name="Раскрыть форму поиска").click()
    await page.wait_for_selector('text="УНП заказчика (организатора)"', state='attached')
    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    input_id = soup.find(lambda tag: tag.name == 'span' and tag.text == 'Предмет закупки').find_parent('tr').find_all('input')[0].attrs
    await page.locator(f"input[name='{input_id['name']}']").click()
    await page.locator(f"input[name='{input_id['name']}']").fill(keyword)
    await page.locator("input[name=\"fra\\:date1\"]").click()
    await page.locator("input[name=\"fra\\:date1\"]").fill(yesterday)
    await page.locator("input[name=\"fra\\:date2\"]").click()
    await page.locator("input[name=\"fra\\:date2\"]").fill(today)
    await page.get_by_role("button", name="Искать").click()

    return page

async def run() -> list[dict[str, list[any]]]:
    """Функция парсинга"""
    global list_of_keywords
    result = []
    async with async_playwright() as playwright:
        for keyword in keywords:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36'

            await page.set_extra_http_headers({'User-Agent': user_agent})

            keyword_dict = {keyword: []}
            page = await step(page, keyword)

            while True:
                page, a_href_page_find = await check_page(page)
                if len(a_href_page_find) == 0:
                    break

                for a_href in a_href_page_find:
                    html_content = await page.content()
                    soup = BeautifulSoup(html_content, 'html.parser')

                    element_id = a_href['id'].replace(':', '\\:').replace('\u0000', '')
                    element = await page.query_selector(f'#{element_id}')
                    await element.click()

                    await page.wait_for_url('https://zakupki.butb.by/auctions/viewinvitation.html')

                    html_content = await page.content()
                    soup = BeautifulSoup(html_content, 'html.parser')

                    page, list_element = await parse_a_href(page)
                    print(list_element)
                    keyword_dict[keyword].append(list_element)

                    await page.goto("https://zakupki.butb.by/auctions/reestrauctions.html")

            result.append(keyword_dict)
            await context.close()
            await browser.close()
    list_of_keywords = result
    return result

def run_programm():
    """Функция запуска парсера."""
    global id_purchase_list

    db: ParserDelete = ParserDelete.objects.all()
    id_purchase_list = [obj.id_purchase for obj in db]

    def run_async_code() -> list[dict[str, list[any]]]:
        """Функция для асинхронного запуска парсера."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run())
        loop.close()
        return result

    thread = Thread(target=run_async_code)
    thread.start()
    thread.join()

    return list_of_keywords
