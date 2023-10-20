from playwright.sync_api import Playwright, Page, sync_playwright
from settings import today, yesterday, keywords
from bs4 import BeautifulSoup
from time import sleep
import asyncio

list_of_keywords = []


def check_page(page: Page) -> tuple[Page, list]:

    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    a_href_page_find = soup.find(id='fra:auctionList:tbody').find_all('a')

    if len(a_href_page_find) > 10:
        element_id = a_href_page_find[0]['id'].replace(':', '\\:').replace('\u0000', '')
        page.wait_for_selector(f'#{element_id}', state='attached')

    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    a_href_page_find = soup.find(id='fra:auctionList:tbody').find_all('a')

    return (page, a_href_page_find)

def parse_a_href(a_href: str) -> None:
    pass

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
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page = step(page, keyword)


    page, a_href_page_find = check_page(page)

    for a_href in a_href_page_find:
        element_id = a_href['id'].replace(':', '\\:').replace('\u0000', '')
        page.query_selector(f'#{element_id}').click()
        page.wait_for_selector(f'#{element_id}', state='detached')
        page.go_back()


    # ---------------------
    context.close()
    browser.close()


for keyword in keywords:
    with sync_playwright() as playwright:
        run(playwright, keyword)


