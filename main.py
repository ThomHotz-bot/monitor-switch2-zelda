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
    "User-Agent": (
        "Mozilla/5.0"
    )
}

resposta = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Status:", resposta.status_code)

precos = re.findall(
    r'"price"\s*:\s*([0-9]+(?:\.[0-9]+)?)',
    resposta.text
)

print("Preços encontrados:")
print(precos[:20])
