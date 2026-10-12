import pytest

from termometro.scoring import calcular_resultado


def test_procon_tem_prioridade_sobre_tudo():
    resultado = calcular_resultado(na_lista_procon=True, golpe_confirmado=True, dias_de_vida=5000, ip_valido=True)
    assert resultado["score"] == 0
    assert resultado["cor"] == "res-red"
    assert resultado["fonte_principal"] == "procon"
    assert "PROCON" in resultado["status"]


def test_google_tem_prioridade_sobre_idade_e_ip():
    resultado = calcular_resultado(na_lista_procon=False, golpe_confirmado=True, dias_de_vida=5000, ip_valido=True)
    assert resultado["score"] == 0
    assert resultado["cor"] == "res-red"
    assert resultado["fonte_principal"] == "google"
    assert "Google" in resultado["status"]


@pytest.mark.parametrize(
    "dias_de_vida, ip_valido, fonte_esperada",
    [
        (-1, True, "dominio_invalido"),
        (None, True, "dominio_invalido"),
        (100, False, "ip_invalido"),
        (100, True, "idade_dominio"),
    ],
)
def test_fonte_principal_sem_blacklist(dias_de_vida, ip_valido, fonte_esperada):
    resultado = calcular_resultado(False, False, dias_de_vida, ip_valido)
    assert resultado["fonte_principal"] == fonte_esperada


@pytest.mark.parametrize("dias_de_vida", [-1, 0, 1, 12, 92, 180, 365, 10564])
@pytest.mark.parametrize("ip_valido", [True, False])
def test_score_sempre_entre_0_e_100(dias_de_vida, ip_valido):
    resultado = calcular_resultado(False, False, dias_de_vida, ip_valido)
    assert 0 <= resultado["score"] <= 100


def test_dominio_mais_antigo_nunca_pontua_pior_que_mais_novo():
    anterior = -1
    for dias in (0, 1, 10, 30, 92, 180, 365, 1000, 10564):
        atual = calcular_resultado(False, False, dias, ip_valido=True)["score"]
        assert atual >= anterior
        anterior = atual


def test_ip_invalido_nunca_pontua_melhor_que_ip_valido_pra_mesma_idade():
    for dias in (0, 30, 180, 365):
        com_ip = calcular_resultado(False, False, dias, ip_valido=True)["score"]
        sem_ip = calcular_resultado(False, False, dias, ip_valido=False)["score"]
        assert com_ip >= sem_ip


@pytest.mark.parametrize(
    "dias_de_vida, ip_valido, cor_esperada",
    [
        (10564, True, "res-green"),   # domínio bem estabelecido
        (0, True, "res-red"),          # recém-criado, mesmo com IP válido
        (-1, False, "res-red"),        # sem dado nenhum: pior caso
    ],
)
def test_cor_bate_com_a_faixa_do_score(dias_de_vida, ip_valido, cor_esperada):
    resultado = calcular_resultado(False, False, dias_de_vida, ip_valido)
    assert resultado["cor"] == cor_esperada


def test_fatores_explicam_a_combinacao_ponderada_sem_blacklist():
    resultado = calcular_resultado(False, False, 180, ip_valido=True)
    fatores = resultado["fatores"]
    assert len(fatores) == 2
    nomes = {fator["fonte"] for fator in fatores}
    assert nomes == {"idade_dominio", "resolucao_ip"}
    # a soma das contribuições (arredondadas) bate com o score final, a menos
    # de 1 ponto de diferença por arredondamento em separado de cada parcela
    soma_contribuicoes = sum(fator["contribuicao"] for fator in fatores)
    assert abs(soma_contribuicoes - resultado["score"]) <= 1


def test_fatores_da_blacklist_tem_peso_total_e_contribuicao_zero():
    resultado = calcular_resultado(na_lista_procon=True, golpe_confirmado=False, dias_de_vida=5000, ip_valido=True)
    assert len(resultado["fatores"]) == 1
    assert resultado["fatores"][0]["peso"] == 1.0
    assert resultado["fatores"][0]["contribuicao"] == 0
