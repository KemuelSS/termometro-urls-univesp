LIMIAR_MUITO_RECENTE_DIAS = 30
LIMIAR_RECENTE_DIAS = 180


def calcular_resultado(na_lista_procon, golpe_confirmado, dias_de_vida):
    """Motor de regras. Prioridade: Procon > Google Safe Browsing > idade do domínio (WHOIS)."""
    if na_lista_procon:
        return {
            "score": 0,
            "status": "🚨 ALERTA PROCON-SP: Este site consta na lista oficial de sites a evitar (Fraude/Não entrega).",
            "cor": "res-red",
        }

    if golpe_confirmado:
        return {
            "score": 0,
            "status": "PERIGO CRÍTICO: Este link está na lista negra de fraudes do Google!",
            "cor": "res-red",
        }

    if dias_de_vida == -1:
        return {
            "score": 10,
            "status": "Perigo: Domínio inválido, oculto ou suspeito.",
            "cor": "res-red",
        }

    if dias_de_vida < LIMIAR_MUITO_RECENTE_DIAS:
        return {
            "score": 30,
            "status": f"Perigo: Site muito recente ({dias_de_vida} dias). Alto risco.",
            "cor": "res-red",
        }

    if dias_de_vida < LIMIAR_RECENTE_DIAS:
        return {
            "score": 60,
            "status": f"Atenção: Site relativamente novo ({dias_de_vida} dias).",
            "cor": "res-orange",
        }

    return {
        "score": 95,
        "status": f"Seguro: Site estabelecido e antigo ({dias_de_vida} dias).",
        "cor": "res-green",
    }
