import requests
import json
import time

# =============================================================================
# CONFIGURAÇÃO DOS TESTES
# =============================================================================

BASE_URL = "http://127.0.0.1:8080"

ENDPOINT_VENDA = "/api/v1/predicaoVenda"
ENDPOINT_CLIENTE = "/api/v1/classificacaoCliente"
ENDPOINT_DEMANDA = "/api/v1/predicaoDemanda"
ENDPOINT_SENTIMENTO = "/api/v1/classificacaoSentimento"

VALID_TOKEN = "MEU_TOKEN_SECRETO_12345"
INVALID_TOKEN = "TOKEN_QUALQUER_INVALIDO"


# =============================================================================
# FUNÇÃO AUXILIAR PARA CHAMAR A API
# =============================================================================

def call_api(endpoint, payload=None, token=VALID_TOKEN, method='POST'):
    """
    Função genérica para realizar chamadas à API.

    Args:
        endpoint (str): O endpoint do serviço a ser chamado.
        payload (dict, optional): O corpo da requisição em formato de dicionário.
        token (str, optional): O token de autenticação. Pode ser None para testar
                               a ausência do cabeçalho.
        method (str, optional): O método HTTP a ser utilizado ('POST', 'GET', etc.).

    Returns:
        requests.Response: O objeto de resposta da requisição.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        if method.upper() == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(payload) if payload else None, timeout=5)
        elif method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        else:
            response = requests.request(method, url, headers=headers, data=json.dumps(payload) if payload else None, timeout=5)
        return response
    except requests.exceptions.ConnectionError as e:
        print(f"\nERRO DE CONEXÃO: Não foi possível conectar a {url}.")
        print("Por favor, verifique se a sua aplicação Flask (app.py) está em execução.")
        return None


def print_test_result(test_name, response):
    """Formata e exibe o resultado de um teste."""
    if response is None:
        return

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = response.text

    print(f"-> Teste: {test_name:<45} | Status: {response.status_code:<5} | Resposta: {response_data}")


# =============================================================================
# BATERIA DE TESTES
# =============================================================================

def run_authentication_tests():
    """Testa os vários cenários de falha de autenticação."""
    print("\n--- INICIANDO TESTES DE AUTENTICAÇÃO ---")
    
    # Teste 1: Token inválido
    r = call_api(ENDPOINT_VENDA, payload={"mes": 1, "ano": 2024}, token=INVALID_TOKEN)
    print_test_result("Token inválido", r)

    # Teste 2: Token não fornecido
    r = call_api(ENDPOINT_VENDA, payload={"mes": 1, "ano": 2024}, token=None)
    print_test_result("Token ausente", r)

    # Teste 3: Formato do Header 'Authorization' incorreto
    url = f"{BASE_URL}{ENDPOINT_VENDA}"
    headers = {"Authorization": f"Token {VALID_TOKEN}", "Content-Type": "application/json"} # Usando "Token" em vez de "Bearer"
    r = requests.post(url, headers=headers, data=json.dumps({"mes": 1, "ano": 2024}))
    print_test_result("Formato do Header inválido", r)


def run_predicao_venda_tests():
    """Testa o endpoint de Predição de Vendas."""
    print("\n--- INICIANDO TESTES DE PREDIÇÃO DE VENDA ---")
    
    # Teste 1: Requisição válida
    payload = {"mes": 11, "ano": 2025}
    r = call_api(ENDPOINT_VENDA, payload)
    print_test_result("Requisição válida", r)
    
    # Teste 2: Payload com dados inválidos (mês > 12)
    payload = {"mes": 13, "ano": 2024}
    r = call_api(ENDPOINT_VENDA, payload)
    print_test_result("Payload com mês inválido", r)
    
    # Teste 3: Payload com chave faltando ('ano')
    payload = {"mes": 10}
    r = call_api(ENDPOINT_VENDA, payload)
    print_test_result("Payload com chave faltando", r)


def run_classificacao_cliente_tests():
    """Testa o endpoint de Classificação de Cliente."""
    print("\n--- INICIANDO TESTES DE CLASSIFICAÇÃO DE CLIENTE ---")
    
    # Teste 1: Requisição válida com CPF formatado
    payload = {"cpf": "123.456.789-00"}
    r = call_api(ENDPOINT_CLIENTE, payload)
    print_test_result("CPF formatado (final 0 -> Risco Alto)", r)
    
    # Teste 2: Requisição válida com CPF não formatado
    payload = {"cpf": "98765432198"}
    r = call_api(ENDPOINT_CLIENTE, payload)
    print_test_result("CPF não formatado (final 8 -> Risco M. Baixo)", r)

    # Teste 3: CPF inválido (menos de 11 dígitos)
    payload = {"cpf": "12345"}
    r = call_api(ENDPOINT_CLIENTE, payload)
    print_test_result("CPF inválido (curto)", r)


def run_predicao_demanda_tests():
    """Testa o endpoint de Predição de Demanda."""
    print("\n--- INICIANDO TESTES DE PREDIÇÃO DE DEMANDA ---")

    # Teste 1: Requisição válida
    payload = {"produto_id": 852, "periodo": "Próximos 30 dias"}
    r = call_api(ENDPOINT_DEMANDA, payload)
    print_test_result("Requisição válida", r)

    # Teste 2: 'produto_id' não é um número
    payload = {"produto_id": "SKU-ABC", "periodo": "Próxima Semana"}
    r = call_api(ENDPOINT_DEMANDA, payload)
    print_test_result("ID do produto não numérico", r)


def run_classificacao_sentimento_tests():
    """Testa o endpoint de Classificação de Sentimento."""
    print("\n--- INICIANDO TESTES DE CLASSIFICAÇÃO DE SENTIMENTO ---")

    # Teste 1: Sentimento positivo
    payload = {"texto": "Adorei o produto, a entrega foi rápida e o material é de ótima qualidade. Recomendo!"}
    r = call_api(ENDPOINT_SENTIMENTO, payload)
    print_test_result("Sentimento Positivo", r)

    # Teste 2: Sentimento negativo
    payload = {"texto": "Que péssimo, veio com problema e o atendimento foi terrível."}
    r = call_api(ENDPOINT_SENTIMENTO, payload)
    print_test_result("Sentimento Negativo", r)

    # Teste 3: Sentimento neutro
    payload = {"texto": "A embalagem do produto chegou hoje."}
    r = call_api(ENDPOINT_SENTIMENTO, payload)
    print_test_result("Sentimento Neutro", r)

    # Teste 4: Texto vazio
    payload = {"texto": "   "}
    r = call_api(ENDPOINT_SENTIMENTO, payload)
    print_test_result("Texto vazio", r)


# =============================================================================
# EXECUTOR PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=====================================================")
    print("== INICIANDO BATERIA DE TESTES PARA A API DE IA ==")
    print("=====================================================")
    
    time.sleep(1)

    run_authentication_tests()
    run_predicao_venda_tests()
    run_classificacao_cliente_tests()
    run_predicao_demanda_tests()
    run_classificacao_sentimento_tests()

    print("\n=====================================================")
    print("== BATERIA DE TESTES FINALIZADA ==")
    print("=====================================================")
