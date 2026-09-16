from datetime import datetime
import csv
import os
import requests

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

preco_atual = 3999

arquivo = "precos.csv"

if not os.path.exists(arquivo):
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["data", "loja", "preco", "link"])

with open(arquivo, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Teste",
        preco_atual,
        "https://exemplo.com"
    ])

print("Histórico atualizado")

if preco_atual <= PRECO_ALVO:

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    resposta = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"""
🎮 Nintendo Switch 2 Zelda

Preço encontrado: R$ {preco_atual}

Meta: R$ {PRECO_ALVO}

✅ Oferta dentro da meta
"""
        }
    )

    print("Status Telegram:", resposta.status_code)

else:
    print("Preço acima da meta")
