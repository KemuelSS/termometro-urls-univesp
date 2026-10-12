import pytest

from termometro.scoring import calcular_resultado


@pytest.mark.parametrize(
    "na_lista_procon, golpe_confirmado, dias_de_vida, score_esperado, cor_esperada",
    [
        (True, False, 999, 0, "res-red"),      # Procon tem prioridade sobre tudo
        (True, True, 999, 0, "res-red"),
        (False, True, 999, 0, "res-red"),      # Google Safe Browsing
        (False, False, -1, 10, "res-red"),     # domínio inválido/oculto
        (False, False, 0, 30, "res-red"),      # muito recente
        (False, False, 29, 30, "res-red"),     # limite inferior exclusivo
        (False, False, 30, 60, "res-orange"),  # limite exato vira "recente"
        (False, False, 179, 60, "res-orange"),
        (False, False, 180, 95, "res-green"),  # limite exato vira "seguro"
        (False, False, 10564, 95, "res-green"),
    ],
)
def test_calcular_resultado(na_lista_procon, golpe_confirmado, dias_de_vida, score_esperado, cor_esperada):
    resultado = calcular_resultado(na_lista_procon, golpe_confirmado, dias_de_vida)
    assert resultado["score"] == score_esperado
    assert resultado["cor"] == cor_esperada
    assert resultado["status"]


def test_procon_tem_prioridade_sobre_google():
    resultado = calcular_resultado(na_lista_procon=True, golpe_confirmado=True, dias_de_vida=5000)
    assert "PROCON" in resultado["status"]


def test_google_tem_prioridade_sobre_idade_do_dominio():
    resultado = calcular_resultado(na_lista_procon=False, golpe_confirmado=True, dias_de_vida=5000)
    assert "Google" in resultado["status"]
