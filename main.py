from datetime import datetime
import pandas as pd
import os
import requests

ARQUIVO = "precos.csv"

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

# PREÇO DE TESTE
# depois vamos trocar pela captura real
preco_atual = 3999

nova_linha = pd.DataFrame([
    {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "loja": "Teste",
        "preco": preco_atual,
        "link": "https://exemplo.com"
    }
])

if os.path.exists(ARQUIVO):
    historico = pd.read_csv(ARQUIVO)

    historico = pd.concat(
        [historico, nova_linha],
        ignore_index=True
    )
else:
    historico = nova_linha

historico.to_csv(
    ARQUIVO,
    index=False
)

print("Histórico atualizado")

if preco_atual <= PRECO_ALVO:

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"""
🎮 Nintendo Switch 2 Zelda

Preço encontrado:
R$ {preco_atual}

Meta:
R$ {PRECO_ALVO}

✅ Oferta dentro da meta
"""
        }
    )

    print("Alerta enviado")
