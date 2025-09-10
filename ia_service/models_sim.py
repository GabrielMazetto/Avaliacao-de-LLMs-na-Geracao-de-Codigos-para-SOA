# models_sim.py
from typing import Tuple, Dict, Any
import hashlib
import math
from datetime import datetime
import re

def _seed_from_args(*args) -> int:
    joined = "|".join(str(a) for a in args)
    h = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    # converte parte do hash em int
    return int(h[:16], 16)

def _confidence_from_seed(seed: int, low=0.6, high=0.98) -> float:
    # normaliza determinístico entre low e high
    r = (seed % 10000) / 10000.0
    return round(low + (high - low) * r, 3)

# Predição de vendas: mês (1-12) e ano (YYYY)
def predicao_venda(mes: int, ano: int) -> Dict[str, Any]:
    seed = _seed_from_args("predicao_venda", mes, ano)
    # base mensal aleatória determinística
    base = ((ano % 100) * 1000) + (mes * 200) + (seed % 500)
    # adiciona sazonalidade simples (dezembro +20%, jan -10%, jul +10%)
    saz = 1.0
    if mes == 12:
        saz = 1.20
    elif mes == 1:
        saz = 0.90
    elif mes == 7:
        saz = 1.10
    predicted = int(base * saz)
    conf = _confidence_from_seed(seed)
    return {
        "model": "predicaoVenda_sim",
        "mes": mes,
        "ano": ano,
        "predicted_sales": predicted,
        "confidence": conf,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

# Validação simples de CPF (algoritmo oficial)
def _clean_digits(s: str) -> str:
    return "".join(ch for ch in s if ch.isdigit())

def validate_cpf(cpf: str) -> bool:
    cpf = _clean_digits(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    def calc(digs):
        s = sum(int(a) * b for a, b in zip(digs, range(len(digs)+1, 1, -1)))
        r = (s * 10) % 11
        return r if r < 10 else 0
    first = calc(cpf[:9])
    second = calc(cpf[:9] + str(first))
    return cpf[-2:] == f"{first}{second}"

# Classificação de crédito por CPF (simulada determinística)
def classificacao_cliente(cpf: str) -> Dict[str, Any]:
    clean = _clean_digits(cpf)
    valid = validate_cpf(clean)
    seed = _seed_from_args("classificacao_cliente", clean)
    score = seed % 1000  # 0..999
    # mapear para categorias simples
    if score >= 800:
        cat = "A"
        risk = "Baixo"
    elif score >= 600:
        cat = "B"
        risk = "Moderado"
    elif score >= 400:
        cat = "C"
        risk = "Alto"
    else:
        cat = "D"
        risk = "Muito Alto"
    conf = _confidence_from_seed(seed)
    return {
        "model": "classificacaoCliente_sim",
        "cpf": cpf,
        "valid_cpf": valid,
        "score": int(score),
        "category": cat,
        "risk_level": risk,
        "confidence": conf,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

# Predição de demanda por produto e periodo
# period: "YYYY-MM" or "YYYY-MM:YYYY-MM"
def _parse_period(period: str):
    if ":" in period:
        parts = period.split(":")
        if len(parts) != 2:
            raise ValueError("period must be YYYY-MM or YYYY-MM:YYYY-MM")
        start, end = parts
        return start, end
    else:
        return period, period

def _months_between(start: str, end: str):
    # start/end as YYYY-MM
    y1, m1 = map(int, start.split("-"))
    y2, m2 = map(int, end.split("-"))
    months = (y2 - y1) * 12 + (m2 - m1) + 1
    if months < 1:
        raise ValueError("end must be after or equal to start")
    return months

def predicao_demanda(product_id: str, period: str) -> Dict[str, Any]:
    start, end = _parse_period(period)
    months = _months_between(start, end)
    seed = _seed_from_args("predicao_demanda", product_id, start, end)
    # base mensal dependente do product_id hash
    base_unit = 50 + (seed % 200)  # 50..249
    # add small variation across months deterministically
    total = 0
    monthly = []
    for i in range(months):
        s = (seed + i * 97) % 1000
        qty = int(base_unit * (0.8 + (s % 41) / 100.0))  # 0.8..1.2
        monthly.append(qty)
        total += qty
    conf = _confidence_from_seed(seed)
    return {
        "model": "predicaoDemanda_sim",
        "product_id": product_id,
        "period": period,
        "months": months,
        "monthly_estimate": monthly,
        "total_estimate": total,
        "confidence": conf,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

# Classificação de sentimento (simples lexicon)
_POS = {"bom", "ótimo", "otimo", "excelente", "gostei", "adorei", "satisfeito", "fantástico", "positivo", "feliz", "maravilhoso"}
_NEG = {"ruim", "péssimo", "pessimo", "detestei", "ódio", "odio", "insatisfeito", "horrível", "horrivel", "negativo", "triste"}

def classificacao_sentimento(text: str) -> Dict[str, Any]:
    txt = text.lower()
    # token simples
    words = re.findall(r"\w+", txt, flags=re.UNICODE)
    pos = sum(1 for w in words if w in _POS)
    neg = sum(1 for w in words if w in _NEG)
    raw_score = pos - neg  # integer
    # normaliza entre -1 e 1
    if pos + neg == 0:
        score = 0.0
    else:
        score = (raw_score) / (pos + neg)
    # mapa em etiqueta
    if score > 0.3:
        label = "positive"
    elif score < -0.3:
        label = "negative"
    else:
        label = "neutral"
    # confidence depends on number of sentiment words
    conf = round(min(0.99, 0.5 + 0.1 * (pos + neg)), 3)
    return {
        "model": "classificacaoSentimento_sim",
        "text": text,
        "pos_count": pos,
        "neg_count": neg,
        "score": round(score, 3),
        "label": label,
        "confidence": conf,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }