from main.parsers.settings import Settings
import asyncio
import collections
import json
import os.path
import webbrowser
import datetime
from urllib.parse import urlencode
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

MIN_PRICE = 5000
MIN_PRICE_PAGE = 1000

list_result = []

today, yesterday = Settings().date_date()
keywords = Settings().get_keywords()



async def parse_url(page, url):

    url = 'https://goszakupki.by/' + url

    await page.goto(url)

    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(html_content.decode('utf-8'))
    tr_name_company = soup.find(text='Наименование организации')

    return page



async def parse_page(page):

    html_content = await page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    a_href_all = soup.select('table > tbody a')
    tr_all = soup.select('table > tbody tr')

    for a_href, tr in zip(a_href_all, tr_all):
        price = tr.select('td')[5].text.replace(' ', '').replace('\xa0', '').replace('BYN', '')
        if float(price) < MIN_PRICE_PAGE:
            continue

        a_url = a_href['href']

        page = await parse_url(page, a_url)

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
        cache = get_cache()
        for keyword in keywords:
            url = get_url_goszakupki(keyword, from_date, to_date)
            actual_zids, actual_prices = await find_actual_zids(page, url)
            new_zids = set(actual_zids).difference(cache.get(keyword, []))
            if new_zids:
                should_open = True
                should_open &= any([actual_prices[zid] > MIN_PRICE for zid in new_zids])
                if should_open:
                    print(keyword)
                    page = await parse_page(page)
                    webbrowser.get('windows-default').open(url)
            cache[keyword] = actual_zids
        with open("cache.txt", "w") as f:
            json.dump(cache, f)
        await context.close()
        await browser.close()




if __name__ == '__main__':
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    asyncio.get_event_loop().run_until_complete(watchdog_goszakupki(yesterday, today))
