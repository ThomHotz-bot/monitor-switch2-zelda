from playwright.sync_api import sync_playwright
import csv

with open(
    "produtos.csv",
    "r",
    encoding="utf-8"
) as f:

    leitor = csv.DictReader(f)

    produto = next(leitor)

url = produto["url"]

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        url,
        wait_until="networkidle"
    )

    print("URL FINAL:")
    print(page.url)

    print("\nTEXTO DA PÁGINA:\n")

    texto = page.locator("body").inner_text()

    print(texto[:5000])

    browser.close()
