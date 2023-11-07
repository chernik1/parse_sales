import sys
import main.parsers.settings as settings
import asyncio
import collections
import json
import os.path
import datetime
from urllib.parse import urlencode
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from threading import Thread
from main.models import ParserZakuDelete

list_result = []

url_list = []

MIN_PRICE = 5000
MIN_PRICE_PAGE = 1000

today, yesterday = settings.Settings().date_date()
keywords = settings.Settings().get_keywords()

async def form_main_name_purchase(soup):
    tr_all_name_purchase = soup.find_all('table', class_='table table-striped')[0].find_all('tr')
    td_all_name_purchase = soup.find_all('table', class_='table table-striped')[0].find_all('td')
    for index, tr_element in enumerate(tr_all_name_purchase):
        text = tr_element.text.strip()
        if 'Название процедуры закупки из одного источника' in text:
            main_name_purchase = td_all_name_purchase[index].text
            return main_name_purchase, soup
        elif 'Название процедуры закупки' in text:
            main_name_purchase = td_all_name_purchase[index + 1].text
            return main_name_purchase, soup
        elif 'Название запроса ценовых предложений' in text:
            main_name_purchase = td_all_name_purchase[index + 1].text
            return main_name_purchase, soup
        else:
            main_name_purchase = 'Не нашлось'
    return main_name_purchase, soup


async def parse_url(page, url, keyword):
    #global list_result

    url = 'https://goszakupki.by' + url

    await page.goto(url)

    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')

    name_company = soup.find(text='Наименование организации').find_parent('tr').find_all('td')[0].text
    payer_number = soup.find(text='УНП организации').find_parent('tr').find_all('td')[0].text

    main_name_purchase, soup = await form_main_name_purchase(soup)


    price = soup.find(string='Общая ориентировочная стоимость закупки').find_parent('tr').find_all('td')[0].text
    location = soup.find(string='Место нахождения организации').find_parent('tr').find_all('td')[0].text

    list_purchase = []
    all_purchase = soup.find_all('td', class_='lot-description')
    for purchase in all_purchase:
        list_purchase.append(purchase.text)
    name_purchase = ', '.join(list_purchase)

    list_result.append({
        'keyword': keyword,
        'url_purchase': url,
        'name_company': name_company,
        'payer_number': payer_number,
        'main_name_purchase': main_name_purchase,
        'price': price,
        'name_purchase': name_purchase,
        'location': location,
    })

    return page



async def parse_page(page, keyword):

    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    a_href_all = soup.select('table > tbody a')
    tr_all = soup.select('table > tbody tr')

    for a_href, tr in zip(a_href_all, tr_all):
        price = tr.select('td')[5].text.replace(' ', '').replace('\xa0', '').replace('BYN', '')
        if float(price) < MIN_PRICE_PAGE:
            continue

        a_url = a_href['href']

        if a_url in url_list:
            continue

        page = await parse_url(page, a_url, keyword)

    return page

def get_url_goszakupki(text, from_date, to_date):
    params = {
        'TendersSearch[text]': text,
        'TendersSearch[created_from]': from_date.strftime("%d.%m.%Y"),
        'TendersSearch[created_to]': to_date.strftime("%d.%m.%Y")
    }
    return "https://goszakupki.by/tenders/posted?" + urlencode(params)


def get_cache():
    if os.path.exists("cache.txt"):
        with open("cache.txt", "r") as f:
            return json.load(f)
    return collections.defaultdict(lambda: [])


async def find_actual_zids(page, url):
    await page.goto(url)
    print(url)
    await page.wait_for_selector("#w0 > table > tbody > tr")
    items = await page.query_selector_all("#w0 > table > tbody > tr")
    actual_zids = []
    prices = {}
    for i in items:
        zid_obj = await i.query_selector("td:nth-child(1)")
        zid = await zid_obj.text_content()
        if zid == "Ничего не найдено.":
            return [], {}
        price_obj = await i.query_selector("td:nth-child(6)")
        price_str = await price_obj.text_content()
        price = float("".join([s for s in price_str.split() if not s.isalpha()]))
        prices[zid] = price
        actual_zids.append(zid)
    return actual_zids, prices


async def watchdog_goszakupki(from_date, to_date):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36'

        await page.set_extra_http_headers({'User-Agent': user_agent})
        # cache = get_cache()
        for keyword in keywords:
            url = get_url_goszakupki(keyword, from_date, to_date)
            actual_zids, actual_prices = await find_actual_zids(page, url)
            # new_zids = set(actual_zids).difference(cache.get(keyword, []))
            new_zids = actual_zids
            if new_zids:
                should_open = True
                should_open &= any([actual_prices[zid] > MIN_PRICE for zid in new_zids])
                if should_open:
                    page = await parse_page(page, keyword)
        await context.close()
        await browser.close()

def run_programm():
    global url_list
    data_was_deleted_urls = ParserZakuDelete.objects.all()
    url_list = [obj.url for obj in data_was_deleted_urls]

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    def run_async_code():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(watchdog_goszakupki(yesterday, today))
        loop.close()
        return result

    thread = Thread(target=run_async_code)
    thread.start()
    thread.join()

    return list_result

# result = run_programm()
# print(result)
