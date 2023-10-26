from playwright.sync_api import Playwright, Page, sync_playwright
from ..settings import today, yesterday, keywords
from bs4 import BeautifulSoup
from pprint import pprint

list_of_keywords = []







def run(playwright: Playwright, keyword: str) -> None:
    pass

def run_programm():
    global list_of_keywords
    list_of_keywords = []
    for keyword in keywords:
        with sync_playwright() as playwright:
            run(playwright, keyword)

    pprint(list_of_keywords)
    return list_of_keywords

#run_programm()