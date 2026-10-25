import math

# Pesos da combinação ponderada (somam 1.0). Idade do domínio pesa mais que a
# validade do IP porque é o sinal mais discriminante entre os dois: a grande
# maioria dos domínios resolve pra algum IP, válido ou não, então por si só
# esse fator varia pouco; idade é o que de fato separa um golpe recente de um
# site estabelecido.
PESO_IDADE = 0.7
PESO_IP = 0.3

# Curva de saturação exponencial pra idade do domínio: calibrada pra cruzar
# ~60 pontos (de 100) por volta de 180 dias, o mesmo marco que no modelo
# anterior separava "recente" de "estabelecido" — mas aqui sem o salto brusco,
# a transição é suave antes e depois desse marco.
TAU_IDADE_DIAS = 200

LIMIAR_SEGURO = 80
LIMIAR_ATENCAO = 50


def _pontuar_idade(dias_de_vida):
    """0 (recém-criado ou sem data verificável) a 100 (bem estabelecido)."""
    if dias_de_vida is None or dias_de_vida < 0:
        return 0.0
    return 100 * (1 - math.exp(-dias_de_vida / TAU_IDADE_DIAS))


def _pontuar_ip(ip_valido):
    return 100.0 if ip_valido else 0.0


def _fonte_principal(na_lista_procon, golpe_confirmado, dias_de_vida, ip_valido):
    if na_lista_procon:
        return "procon"
    if golpe_confirmado:
        return "google"
    if dias_de_vida is None or dias_de_vida < 0:
        return "dominio_invalido"
    if not ip_valido:
        return "ip_invalido"
    return "idade_dominio"


def calcular_resultado(na_lista_procon, golpe_confirmado, dias_de_vida, ip_valido=True):
    """Motor de regras. Procon e Google Safe Browsing são sinais de lista
    negra confirmada: qualquer um dos dois zera o score na hora, sem entrar
    na média ponderada (misturar um "confirmado fraudulento" com sinais mais
    fracos deixaria o resultado perigosamente mais brando do que deveria).

    Sem nenhum dos dois, o score é uma combinação ponderada e contínua entre
    a idade do domínio (WHOIS) e a validade da resolução de IP, substituindo
    os 5 valores fixos da versão anterior por uma nota de 0 a 100 — o mesmo
    `dias_de_vida` agora produz notas diferentes em vez de cair sempre na
    mesma faixa."""
    fonte_principal = _fonte_principal(na_lista_procon, golpe_confirmado, dias_de_vida, ip_valido)

    if na_lista_procon:
        return {
            "score": 0,
            "status": "🚨 ALERTA PROCON-SP: Este site consta na lista oficial de sites a evitar (Fraude/Não entrega).",
            "cor": "res-red",
            "fonte_principal": fonte_principal,
            "fatores": [
                {
                    "fonte": "procon",
                    "descricao": "Site consta na lista oficial do Procon-SP.",
                    "peso": 1.0,
                    "pontuacao": 0,
                    "contribuicao": 0,
                }
            ],
        }

    if golpe_confirmado:
        return {
            "score": 0,
            "status": "PERIGO CRÍTICO: Este link está na lista negra de fraudes do Google!",
            "cor": "res-red",
            "fonte_principal": fonte_principal,
            "fatores": [
                {
                    "fonte": "google",
                    "descricao": "URL está na lista negra do Google Safe Browsing.",
                    "peso": 1.0,
                    "pontuacao": 0,
                    "contribuicao": 0,
                }
            ],
        }

    pontos_idade = _pontuar_idade(dias_de_vida)
    pontos_ip = _pontuar_ip(ip_valido)
    score = round(PESO_IDADE * pontos_idade + PESO_IP * pontos_ip)

    idade_valida = dias_de_vida is not None and dias_de_vida >= 0
    detalhes = []
    detalhes.append(f"domínio com {dias_de_vida} dias" if idade_valida else "idade do domínio não verificável")
    if not ip_valido:
        detalhes.append("IP não resolvido")
    detalhe_txt = "; ".join(detalhes)

    if score >= LIMIAR_SEGURO:
        status, cor = f"Seguro: Site estabelecido ({detalhe_txt}).", "res-green"
    elif score >= LIMIAR_ATENCAO:
        status, cor = f"Atenção: Site relativamente novo ({detalhe_txt}).", "res-orange"
    else:
        status, cor = f"Perigo: Alto risco ({detalhe_txt}).", "res-red"

    fatores = [
        {
            "fonte": "idade_dominio",
            "descricao": f"Domínio criado há {dias_de_vida} dias" if idade_valida else "Data de criação do domínio não encontrada no WHOIS",
            "peso": PESO_IDADE,
            "pontuacao": round(pontos_idade),
            "contribuicao": round(PESO_IDADE * pontos_idade),
        },
        {
            "fonte": "resolucao_ip",
            "descricao": "IP do servidor resolvido normalmente" if ip_valido else "IP não pôde ser resolvido (domínio inválido, oculto ou interno)",
            "peso": PESO_IP,
            "pontuacao": round(pontos_ip),
            "contribuicao": round(PESO_IP * pontos_ip),
        },
    ]

    return {
        "score": score,
        "status": status,
        "cor": cor,
        "fonte_principal": fonte_principal,
        "fatores": fatores,
    }
