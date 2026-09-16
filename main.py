from datetime import datetime
from bs4 import BeautifulSoup
import csv
import os
import requests

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

ARQUIVO_PRODUTOS = "produtos.csv"
ARQUIVO_PRECOS = "precos.csv"


def buscar_preco_mercadolivre(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    resposta = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("Status página:", resposta.status_code)

    soup = BeautifulSoup(
        resposta.text,
        "lxml"
    )

    meta = soup.find(
        "meta",
        attrs={"itemprop": "price"}
    )

    if meta:
        return float(meta["content"])

    return None


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

print("Produto:", nome_produto)

preco_avista = buscar_preco_mercadolivre(url)

print("Preço encontrado:", preco_avista)

if preco_avista is None:
    raise Exception(
        "Não foi possível localizar o preço."
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

    leitor = list(csv.DictReader(f))

    if leitor:

        try:
            ultimo_preco = float(
                leitor[-1]["preco_avista"]
            )
        except:
            pass

        try:

            precos = [
                float(x["preco_avista"])
                for x in leitor
            ]

            menor_preco_historico = min(
                precos
            )

        except:
            pass

if ultimo_preco == preco_avista:

    print(
        "Preço igual ao último registro."
    )

    quit()

novo_recorde = False

if (
    menor_preco_historico is not None
    and preco_avista < menor_preco_historico
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
            "text": f"""
🏆 NOVO MENOR PREÇO HISTÓRICO

{nome_produto}

Loja:
{fonte}

Preço:
R$ {preco_avista}

Link:
{url}
"""
        }
    )

elif preco_avista <= PRECO_ALVO:

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"""
🎮 PREÇO DENTRO DA META

{nome_produto}

Loja:
{fonte}

Preço:
R$ {preco_avista}

Meta:
R$ {PRECO_ALVO}

Link:
{url}
"""
        }
    )
