from datetime import datetime
import csv
import os
import requests

PRODUTO = "Nintendo Switch 2 Zelda 40 Anos"

PRECO_ALVO = float(os.getenv("PRICE_TARGET", 3799))

# PREÇO DE TESTE
preco_avista = 3899
parcelas = "10x 429,90"
total_parcelado = 4299

arquivo = "precos.csv"

menor_preco_historico = None

if os.path.exists(arquivo):

    with open(arquivo, "r", encoding="utf-8") as f:

        leitor = csv.DictReader(f)

        precos = []

        for linha in leitor:

            try:
                precos.append(
                    float(linha["preco_avista"])
                )
            except:
                pass

        if precos:
            menor_preco_historico = min(precos)

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
        "https://exemplo.com"
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

else:

    print(
        f"Menor preço histórico: "
        f"{menor_preco_historico}"
    )
