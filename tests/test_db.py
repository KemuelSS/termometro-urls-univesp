from termometro.db import estatisticas_dashboard, salvar_consulta


def test_estatisticas_vazio(app):
    stats = estatisticas_dashboard()
    assert stats["total"] == 0
    assert stats["top_dominios"] == []
    assert stats["fontes"] == {}


def test_estatisticas_distribuicao_por_faixa(app):
    salvar_consulta("https://seguro.example", 90, "idade_dominio")
    salvar_consulta("https://atencao.example", 60, "idade_dominio")
    salvar_consulta("https://perigo.example", 10, "idade_dominio")

    stats = estatisticas_dashboard()
    assert stats["total"] == 3
    assert stats["faixas_score"]["seguro (80-100)"] == 1
    assert stats["faixas_score"]["atenção (50-79)"] == 1
    assert stats["faixas_score"]["perigo (0-49)"] == 1


def test_estatisticas_top_dominios_ordenado_por_frequencia(app):
    salvar_consulta("https://mais-consultado.example", 50, "idade_dominio")
    salvar_consulta("https://mais-consultado.example", 50, "idade_dominio")
    salvar_consulta("https://mais-consultado.example", 50, "idade_dominio")
    salvar_consulta("https://pouco-consultado.example", 50, "idade_dominio")

    stats = estatisticas_dashboard()
    assert stats["top_dominios"][0] == ("https://mais-consultado.example", 3)
    assert stats["top_dominios"][1] == ("https://pouco-consultado.example", 1)


def test_estatisticas_taxa_por_fonte(app):
    salvar_consulta("https://a.example", 0, "procon")
    salvar_consulta("https://b.example", 0, "google")
    salvar_consulta("https://c.example", 70, "idade_dominio")
    salvar_consulta("https://d.example", 70, "idade_dominio")

    stats = estatisticas_dashboard()
    assert stats["fontes"] == {"procon": 1, "google": 1, "idade_dominio": 2}
