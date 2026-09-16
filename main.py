from datetime import datetime
import csv
import os
import requests

PRODUTO = "Nintendo Switch 2 Zelda 40 Anos"

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

# DADOS DE TESTE
preco_avista = 3999
parcelas = "10x 429,90"
total_parcelado = 4299

arquivo = "precos.csv"

if not os.path.exists(arquivo):
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "data",
            "produto",
            "loja",
            "preco_avista",
            "parcelas",
            "total_parcelado",
            "link"
        ])

with open(arquivo, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        PRODUTO,
        "Teste",
        preco_avista,
        parcelas,
        total_parcelado,
        "https://exemplo.com"
    ])

print("Histórico atualizado")

if preco_avista <= PRECO_ALVO:

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"""
🎮 {PRODUTO}

Preço à vista:
R$ {preco_avista}

Parcelamento:
{parcelas}

Meta:
R$ {PRECO_ALVO}

✅ Oferta dentro da meta
"""
        }
    )
