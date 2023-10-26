from playwright.sync_api import Playwright, Page, sync_playwright
from ..settings import today, yesterday, keywords
from bs4 import BeautifulSoup
from pprint import pprint
#from settings import today, yesterday, keywords

list_of_keywords = []

def check_page(page: Page) -> tuple[Page, list]:

    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    a_href_page_find = soup.find(id='fra:auctionList:tbody')
    if a_href_page_find is None:
        return (page, [])
    a_href_page_find = a_href_page_find.find_all('a')

    if len(a_href_page_find) == 20:
        element_id = a_href_page_find[18]['id'].replace(':', '\\:').replace('\u0000', '')
        page.wait_for_selector(f'#{element_id}', state='detached')

        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        a_href_page_find = soup.find(id='fra:auctionList:tbody')
        if a_href_page_find is None:
            return (page, [])
        a_href_page_find = a_href_page_find.find_all('a')

        return (page, a_href_page_find)

    return (page, [])


def parse_a_href(page: Page) -> tuple[Page, list]:
    list_of_objects = []

    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')

    register = soup(text='Регистрационный номер')
    register_tr = register[0].find_parent('tr')
    register_all_span = register_tr.find_all('span')
    register_text = register_all_span[1].text
    list_of_objects.append(register_text)

    name_company = soup(text='Полное наименование')
    name_company_tr = name_company[1].find_parent('tr')
    name_company_all_span = name_company_tr.find_all('span')
    name_company_text = name_company_all_span[1].text
    list_of_objects.append(name_company_text)

    date = soup(text='Дата размещения приглашения')
    date_tr = date[0].find_parent('tr')
    date_all_span = date_tr.find_all('span')
    date_text = date_all_span[1].text
    list_of_objects.append(date_text)

    name_purchase = soup(text='Наименование закупки')
    name_purchase_tr = name_purchase[0].find_parent('tr')
    name_purchase_all_span = name_purchase_tr.find_all('span')
    name_purchase_text = name_purchase_all_span[1].text
    list_of_objects.append(name_purchase_text)

    price = soup(text='Ориентировочная стоимость закупки')
    price_tr = price[0].find_parent('tr')
    price_all_span = price_tr.find_all('span')
    price_text = price_all_span[1].text
    price_text = price_text.replace("\xa0", "").replace("\\xa", "")
    list_of_objects.append(price_text)

    payer_account_num = soup(text='УНП')
    payer_account_num_tr = payer_account_num[1].find_parent('tr')
    payer_account_num_all_span = payer_account_num_tr.find_all('span')
    payer_account_num_text = payer_account_num_all_span[1].text
    list_of_objects.append(payer_account_num_text)

    return (page, list_of_objects)





def step(page: Page, keyword: str) -> Page:

    page.goto("https://zakupki.butb.by/auctions/reestrauctions.html")
    page.get_by_role("link", name="Раскрыть форму поиска").click()
    page.locator("input[name=\"fra\\:j_idt174\"]").click()
    page.locator("input[name=\"fra\\:j_idt174\"]").fill(keyword)
    page.locator("input[name=\"fra\\:date1\"]").click()
    page.locator("input[name=\"fra\\:date1\"]").fill(yesterday)
    page.locator("input[name=\"fra\\:date2\"]").click()
    page.locator("input[name=\"fra\\:date2\"]").fill(today)
    page.get_by_role("button", name="Искать").click()

    return page

def run(playwright: Playwright, keyword: str) -> None:
    global list_of_keywords
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page = step(page, keyword)
    keyword_dict = {}
    keyword_dict[keyword] = []

    page, a_href_page_find = check_page(page)

    if len(a_href_page_find) > 0:
        for a_href in a_href_page_find:
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')

            element_id = a_href['id'].replace(':', '\\:').replace('\u0000', '')
            page.query_selector(f'#{element_id}').click()

            page.wait_for_url('https://zakupki.butb.by/auctions/viewinvitation.html')

            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')


            page, list_element = parse_a_href(page)
            keyword_dict[keyword].append(list_element)

            context.close()
            browser.close()

            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page = step(page, keyword)

    list_of_keywords.append(keyword_dict)
    # ---------------------
    context.close()
    browser.close()

def run_programm():
    global list_of_keywords
    list_of_keywords = []
    for keyword in keywords:
        with sync_playwright() as playwright:
            run(playwright, keyword)

    pprint(list_of_keywords)
    return list_of_keywords

#run_programm()
