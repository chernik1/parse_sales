from playwright.sync_api import Playwright, sync_playwright, expect, Page
from settings import today, yesterday, keywords
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://zakupki.butb.by/auctions/reestrauctions.html")
    page.get_by_role("link", name="Раскрыть форму поиска").click()
    page.locator("input[name=\"fra\\:j_idt174\"]").click()
    page.locator("input[name=\"fra\\:j_idt174\"]").press("CapsLock")
    page.locator("input[name=\"fra\\:j_idt174\"]").fill("ЭВМ")
    page.locator("input[name=\"fra\\:j_idt174\"]").press("CapsLock")
    page.locator("input[name=\"fra\\:date1\"]").click()
    page.locator("input[name=\"fra\\:date1\"]").fill("18.10.2023")
    page.locator("input[name=\"fra\\:date2\"]").click()
    page.locator("input[name=\"fra\\:date2\"]").fill("19.10.2023")
    page.get_by_role("button", name="Искать").click()
    page.get_by_role("link", name="ПЭВМ").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

