import requests
import json

BASE_URL = "http://127.0.0.1:8000"
VALID_TOKEN = "secrettoken123"
INVALID_TOKEN = "tokenInvalido"

def call_api(endpoint, payload=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token is not None:
        headers["Authorization"] = token
    resp = requests.post(url, headers=headers, data=json.dumps(payload) if payload else None)
    return resp

# ---------------------------
# 1. Testes de Autenticação
# ---------------------------

def test_auth_token_invalido():
    r = call_api("/predicaoVenda", {"mes":12,"ano":2025}, token=f"Bearer {INVALID_TOKEN}")
    assert r.status_code == 401

def test_auth_token_ausente():
    r = call_api("/predicaoVenda", {"mes":12,"ano":2025}, token=None)
    assert r.status_code == 401

def test_auth_header_invalido():
    r = call_api("/predicaoVenda", {"mes":12,"ano":2025}, token=f"Token {VALID_TOKEN}")
    assert r.status_code == 401

# ------------------------------------
# 2. Testes do Serviço de Predição de Venda
# ------------------------------------

def test_predicao_venda_valida():
    r = call_api("/predicaoVenda", {"mes":12,"ano":2025}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert "predicted_sales" in r.json()

def test_predicao_venda_mes_invalido():
    r = call_api("/predicaoVenda", {"mes":13,"ano":2025}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 422

def test_predicao_venda_chave_faltando():
    r = call_api("/predicaoVenda", {"mes":12}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 422

# ------------------------------------
# 3. Testes do Serviço de Classificação de Cliente
# ------------------------------------

def test_classificacao_cliente_cpf_formatado():
    r = call_api("/classificacaoCliente", {"cpf":"111.444.777-35"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert "score" in r.json() and "category" in r.json()

def test_classificacao_cliente_cpf_nao_formatado():
    r = call_api("/classificacaoCliente", {"cpf":"11144477735"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert "score" in r.json() and "category" in r.json()

def test_classificacao_cliente_cpf_invalido_curto():
    r = call_api("/classificacaoCliente", {"cpf":"12345"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert "score" in r.json() and "category" in r.json()

# ------------------------------------
# 4. Testes do Serviço de Predição de Demanda
# ------------------------------------

def test_predicao_demanda_valida():
    r = call_api("/predicaoDemanda", {"product_id":123,"period":"2025-09:2025-11"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert "total_estimate" in r.json()

def test_predicao_demanda_id_nao_numerico():
    r = call_api("/predicaoDemanda", {"product_id":"SKU-ABC","period":"2025-09:2025-11"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert "total_estimate" in r.json()

# ------------------------------------
# 5. Testes do Serviço de Classificação de Sentimento
# ------------------------------------

def test_sentimento_positivo():
    r = call_api("/classificacaoSentimento", {"text":"Adorei o produto, foi ótimo e excelente!"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert r.json().get("label") == "positive"

def test_sentimento_negativo():
    r = call_api("/classificacaoSentimento", {"text":"O produto foi péssimo e terrível!"}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert r.json().get("label") == "negative"

def test_sentimento_neutro():
    r = call_api("/classificacaoSentimento", {"text":"O produto chegou hoje."}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert r.json().get("label") == "neutral"

def test_sentimento_texto_vazio():
    r = call_api("/classificacaoSentimento", {"text":"   "}, token=f"Bearer {VALID_TOKEN}")
    assert r.status_code == 200
    assert r.json().get("label") == "neutral"

# ---------------------------
# Executar todos os testes
# ---------------------------

if __name__ == "__main__":
    print("==== Iniciando Testes ====")
    test_auth_token_invalido()
    test_auth_token_ausente()
    test_auth_header_invalido()
    test_predicao_venda_valida()
    test_predicao_venda_mes_invalido()
    test_predicao_venda_chave_faltando()
    test_classificacao_cliente_cpf_formatado()
    test_classificacao_cliente_cpf_nao_formatado()
    test_classificacao_cliente_cpf_invalido_curto()
    test_predicao_demanda_valida()
    test_predicao_demanda_id_nao_numerico()
    test_sentimento_positivo()
    test_sentimento_negativo()
    test_sentimento_neutro()
    test_sentimento_texto_vazio()
    print("==== Testes Finalizados ====")
