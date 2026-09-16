from datetime import datetime
from playwright.sync_api import sync_playwright
import csv
import os
import re
import requests

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

ARQUIVO_PRODUTOS = "produtos.csv"
ARQUIVO_PRECOS = "precos.csv"


def obter_preco_kabum(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            url,
            wait_until="networkidle"
        )

        texto = page.locator(
            "body"
        ).inner_text()

        browser.close()

    valores = re.findall(
        r"[0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2}",
        texto
    )

    if not valores:
        return None

    preco = valores[0]

    preco = (
        preco
        .replace(".", "")
        .replace(",", ".")
    )

    return float(preco)


with open(
    ARQUIVO_PRODUTOS,
    "r",
    encoding="utf-8"
) as f:

    leitor = csv.DictReader(f)

    produto = next(leitor)

nome_produto = produto["produto"]
fonte = produto["fonte"]
url = produto["url"]

preco_avista = obter_preco_kabum(
    url
)

print(
    "Preço encontrado:",
    preco_avista
)

if preco_avista is None:
    raise Exception(
        "Preço não encontrado."
    )

parcelas = "-"
total_parcelado = preco_avista

ultimo_preco = None
menor_preco_historico = None

with open(
    ARQUIVO_PRECOS,
    "r",
    encoding="utf-8"
) as f:

    historico = list(
        csv.DictReader(f)
    )

if historico:

    try:
        ultimo_preco = float(
            historico[-1][
                "preco_avista"
            ]
        )
    except:
        pass

    try:
        precos = [
            float(
                linha[
                    "preco_avista"
                ]
            )
            for linha in historico
        ]

        menor_preco_historico = min(
            precos
        )
    except:
        pass

if ultimo_preco == preco_avista:

    print(
        "Preço não mudou."
    )

    quit()

novo_recorde = False

if (
    menor_preco_historico
    is not None
    and
    preco_avista
    < menor_preco_historico
):
    novo_recorde = True

with open(
    ARQUIVO_PRECOS,
    "a",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
        nome_produto,
        fonte,
        preco_avista,
        parcelas,
        total_parcelado,
        url,
        fonte
    ])

token = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

chat_id = os.getenv(
    "TELEGRAM_CHAT_ID"
)

if novo_recorde:

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text":
                f"🏆 NOVO MENOR PREÇO HISTÓRICO\n\n"
                f"{nome_produto}\n\n"
                f"Loja: {fonte}\n"
                f"Preço: R$ {preco_avista}"
        }
    )

elif preco_avista <= PRECO_ALVO:

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text":
                f"🎮 PREÇO DENTRO DA META\n\n"
                f"{nome_produto}\n\n"
                f"Loja: {fonte}\n"
                f"Preço: R$ {preco_avista}"
        }
    )

print(
    "Histórico atualizado."
)
