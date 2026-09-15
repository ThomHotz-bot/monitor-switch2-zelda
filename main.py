import os
import requests

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print("TOKEN EXISTE:", bool(token))
print("CHAT ID EXISTE:", bool(chat_id))

url = f"https://api.telegram.org/bot{token}/sendMessage"

resposta = requests.post(
    url,
    json={
        "chat_id": chat_id,
        "text": "🚀 Teste GitHub Actions"
    }
)

print("STATUS:", resposta.status_code)
print("RESPOSTA:", resposta.text)
