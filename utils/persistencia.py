import json
import os

ARQUIVO_ITENS = os.path.join(os.path.dirname(__file__), '../data/itens.json')

def carregar_itens():
    if not os.path.exists(ARQUIVO_ITENS):
        return []
    with open(ARQUIVO_ITENS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_itens(itens):
    with open(ARQUIVO_ITENS, 'w', encoding='utf-8') as f:
        json.dump(itens, f, ensure_ascii=False, indent=4)