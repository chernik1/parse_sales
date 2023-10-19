from playwright.sync_api import Playwright, sync_playwright, expect, Page
from settings import today, yesterday, keywords
from bs4 import BeautifulSoup

list_of_keywords = []

def run(playwright: Playwright, keyword: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://zakupki.butb.by/auctions/reestrauctions.html")
    page.get_by_role("link", name="Раскрыть форму поиска").click()
    page.locator("input[name=\"fra\\:j_idt174\"]").click()
    page.locator("input[name=\"fra\\:j_idt174\"]").fill(keyword)
    page.locator("input[name=\"fra\\:date1\"]").click()
    page.locator("input[name=\"fra\\:date1\"]").fill(yesterday)
    page.locator("input[name=\"fra\\:date2\"]").click()
    page.locator("input[name=\"fra\\:date2\"]").fill(today)
    page.get_by_role("button", name="Искать").click()

    soup = BeautifulSoup(page.content(), "html.parser")
    a = soup.find(id='fra:auctionList:tbody').find_all('a')

    # ---------------------
    context.close()
    browser.close()


for keyword in keywords:
    with sync_playwright() as playwright:
        run(playwright, keyword)


