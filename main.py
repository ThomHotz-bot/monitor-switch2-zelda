import os
import requests

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    print("Token existe:", bool(token))
    print("Chat ID existe:", bool(chat_id))

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    resposta = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": mensagem
        }
    )

    print("Status:", resposta.status_code)
    print("Resposta:", resposta.text)

def verificar_preco():
    mensagem = """
🎮 TESTE MONITOR SWITCH 2 ZELDA

Se você recebeu esta mensagem,
o GitHub Actions e o Telegram estão funcionando.
"""

    enviar_telegram(mensagem)

if __name__ == "__main__":
    verificar_preco()
`
