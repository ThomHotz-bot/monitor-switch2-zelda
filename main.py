from playwright.sync_api import sync_playwright
import csv
import re

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

    texto = page.locator("body").inner_text()

    browser.close()

print("PROCURANDO VALORES...")

valores = re.findall(
    r"[0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2}",
    texto
)

print("VALORES ENCONTRADOS:")
print(valores[:50])
