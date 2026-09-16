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
            "(Windows NT 10.0; Win64; x64)"
        )
    }

    resposta = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("Status página:", resposta.status_code)

    texto = resposta.text

    print("\n===== INÍCIO DO HTML =====\n")
    print(texto[:5000])
    print("\n===== FIM DO TRECHO =====\n")

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

raise Exception(
    "TESTE DE DIAGNÓSTICO FINALIZADO"
)
