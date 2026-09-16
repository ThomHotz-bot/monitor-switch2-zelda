from datetime import datetime
import csv
import os
import requests

PRODUTO = "Nintendo Switch 2 Zelda 40 Anos"

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

# PREÇO DE TESTE
preco_avista = 3799
parcelas = "10x 429,90"
total_parcelado = 4299

arquivo = "precos.csv"

ultimo_preco = None
menor_preco_historico = None

if os.path.exists(arquivo):

    with open(arquivo, "r", encoding="utf-8") as f:

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

                menor_preco_historico = min(precos)

            except:
                pass

if ultimo_preco == preco_avista:

    print(
        "Preço igual ao último registro."
    )

    print(
        "Nenhuma ação necessária."
    )

    exit()

novo_recorde = False

if (
    menor_preco_historico is not None
    and preco_avista < menor_preco_historico
):
    novo_recorde = True

with open(
    arquivo,
    "a",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        PRODUTO,
        "Teste",
        preco_avista,
        parcelas,
        total_parcelado,
        "https://exemplo.com",
        "Teste"
    ])

print("Histórico atualizado")

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

if novo_recorde:

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"""
🏆 NOVO MENOR PREÇO HISTÓRICO

{PRODUTO}

Novo preço:
R$ {preco_avista}

Menor preço anterior:
R$ {menor_preco_historico}
"""
        }
    )

    print("Novo recorde encontrado")

elif preco_avista <= PRECO_ALVO:

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"""
🎮 {PRODUTO}

Preço:
R$ {preco_avista}

Meta:
R$ {PRECO_ALVO}

✅ Oferta dentro da meta
"""
        }
    )

    print("Oferta dentro da meta")
