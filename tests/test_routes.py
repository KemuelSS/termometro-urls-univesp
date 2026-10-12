from unittest import mock

import termometro.routes as troutes


def mocks_para(ip=None, dias=95, google=False, procon_blocklist=frozenset()):
    return (
        mock.patch.object(troutes, "resolver_ip", return_value=ip),
        mock.patch.object(troutes, "consultar_google_safe_browsing", return_value=google),
        mock.patch.object(troutes, "verificar_idade_dominio", return_value=dias),
        mock.patch.object(troutes, "PROCON_BLOCKLIST", procon_blocklist),
    )


def test_get_index_sem_consultas_anteriores(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Termômetro de URLs" in resp.get_data(as_text=True)


def test_post_url_vazia_nao_quebra(client):
    resp = client.post("/", data={"url": ""})
    assert resp.status_code == 200
    assert "Resultado da Análise" not in resp.get_data(as_text=True)


def test_post_url_segura(client):
    patches = mocks_para(ip="172.217.29.78", dias=10564, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/", data={"url": "https://www.google.com"})
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Seguro" in html
    assert "100/100" in html
    assert "172.217.29.78" in html


def test_post_url_perigo_dominio_recente(client):
    patches = mocks_para(ip="203.0.113.57", dias=12, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/", data={"url": "https://loja-ofertas-relampago.example"})
    html = resp.get_data(as_text=True)
    assert "Perigo" in html
    assert "34/100" in html


def test_post_url_dominio_invalido(client):
    patches = mocks_para(ip=None, dias=-1, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/", data={"url": "https://conta-bloqueada-verificar.example"})
    html = resp.get_data(as_text=True)
    assert "idade do domínio não verificável" in html
    assert "0/100" in html
    assert "IP Indisponível" in html


def test_post_url_barrada_pelo_google(client):
    patches = mocks_para(ip="203.0.113.71", dias=45, google=True)
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/", data={"url": "https://premio-exclusivo-hoje.example"})
    html = resp.get_data(as_text=True)
    assert "lista negra de fraudes do Google" in html
    assert "0/100" in html


def test_post_url_na_lista_procon(client):
    patches = mocks_para(ip="203.0.113.90", dias=0, google=False, procon_blocklist={"loja-fraudulenta.example"})
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/", data={"url": "https://loja-fraudulenta.example"})
    html = resp.get_data(as_text=True)
    assert "ALERTA PROCON-SP" in html
    assert "0/100" in html


def test_api_analisar_url_vazia_retorna_400(client):
    resp = client.post("/api/analisar", data={"url": ""})
    assert resp.status_code == 400
    assert "erro" in resp.get_json()


def test_api_analisar_retorna_json_do_resultado(client):
    patches = mocks_para(ip="172.217.29.78", dias=10564, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/api/analisar", data={"url": "https://www.google.com"})
    assert resp.status_code == 200
    corpo = resp.get_json()
    assert corpo["resultado"]["score"] == 100
    assert corpo["resultado"]["cor"] == "res-green"
    assert corpo["ip_site"] == "172.217.29.78"
    assert corpo["historico"][0]["url"] == "https://www.google.com"


def test_api_analisar_perigo(client):
    patches = mocks_para(ip="203.0.113.57", dias=12, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        resp = client.post("/api/analisar", data={"url": "https://loja-ofertas-relampago.example"})
    corpo = resp.get_json()
    assert corpo["resultado"]["score"] == 34
    assert "Perigo" in corpo["resultado"]["status"]


def test_dashboard_sem_consultas(client):
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert "Ainda não há consultas" in resp.get_data(as_text=True)


def test_dashboard_com_consultas(client):
    patches = mocks_para(ip="203.0.113.90", dias=0, google=False, procon_blocklist={"loja-fraudulenta.example"})
    with patches[0], patches[1], patches[2], patches[3]:
        client.post("/", data={"url": "https://loja-fraudulenta.example"})

    patches = mocks_para(ip="172.217.29.78", dias=10564, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        client.post("/", data={"url": "https://www.google.com"})
        client.post("/", data={"url": "https://www.google.com"})

    resp = client.get("/dashboard")
    html = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert "Total de consultas registradas: <strong>3</strong>" in html
    assert "www.google.com" in html
    assert "procon" in html


def test_historico_aparece_apos_consulta(client):
    patches = mocks_para(ip="172.217.29.78", dias=10564, google=False)
    with patches[0], patches[1], patches[2], patches[3]:
        client.post("/", data={"url": "https://www.google.com"})
        resp = client.post("/", data={"url": "https://www.google.com"})
    html = resp.get_data(as_text=True)
    assert "Últimas Consultas" in html
    assert html.count("www.google.com") >= 2
