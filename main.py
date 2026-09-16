import csv
import requests
import re

with open(
    "produtos.csv",
    "r",
    encoding="utf-8"
) as f:

    leitor = csv.DictReader(f)

    produto = next(leitor)

url = produto["url"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

resposta = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Status:", resposta.status_code)

texto = resposta.text

print("\n=== BUSCANDO REFERÊNCIAS DE PREÇO ===\n")

padroes = [
    r'price',
    r'PRICE',
    r'amount',
    r'currency',
    r'offers'
]

for padrao in padroes:

    print(f"\n--- {padrao} ---")

    encontrados = re.findall(
        rf'.{{0,100}}{padrao}.{{0,100}}',
        texto,
        re.IGNORECASE
    )

    for item in encontrados[:10]:
        print(item)
