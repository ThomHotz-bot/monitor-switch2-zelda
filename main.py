import os
import requests

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": mensagem
        }
    )

def verificar_preco():
    preco_encontrado = 3799

    if preco_encontrado <= PRECO_ALVO:
        mensagem = f'''
🎮 ALERTA SWITCH 2 ZELDA

Preço encontrado:
R$ {preco_encontrado}

Meta:
R$ {PRECO_ALVO}

✅ Hora de verificar a oferta
'''

        enviar_telegram(mensagem)

if __name__ == "__main__":
    verificar_preco()
