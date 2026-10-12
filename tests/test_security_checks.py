import socket
from datetime import datetime, timedelta
from unittest import mock

import pytest

from termometro.security_checks import (
    consultar_google_safe_browsing,
    extrair_dominio,
    resolver_ip,
    verificar_idade_dominio,
)


@pytest.mark.parametrize(
    "url, dominio_esperado",
    [
        ("https://www.google.com", "google.com"),
        ("https://exemplo.com.br/pagina?x=1", "exemplo.com.br"),
        ("http://sub.dominio.com/", "sub.dominio.com"),
        ("dominio-sem-protocolo.com", "dominio-sem-protocolo.com"),
    ],
)
def test_extrair_dominio(url, dominio_esperado):
    assert extrair_dominio(url) == dominio_esperado


def test_resolver_ip_publico():
    with mock.patch("termometro.security_checks.socket.gethostbyname", return_value="8.8.8.8"):
        assert resolver_ip("exemplo.com") == "8.8.8.8"


def test_resolver_ip_privado_vira_invalido():
    with mock.patch("termometro.security_checks.socket.gethostbyname", return_value="192.168.0.1"):
        assert resolver_ip("intranet.local") is None


def test_resolver_ip_loopback_vira_invalido():
    with mock.patch("termometro.security_checks.socket.gethostbyname", return_value="127.0.0.1"):
        assert resolver_ip("localhost") is None


def test_resolver_ip_dominio_inexistente():
    with mock.patch("termometro.security_checks.socket.gethostbyname", side_effect=socket.gaierror):
        assert resolver_ip("nao-existe.invalido") is None


def test_verificar_idade_dominio_antigo():
    criado_em = datetime.now() - timedelta(days=500)
    fake_whois = mock.Mock(creation_date=criado_em)
    with mock.patch("termometro.security_checks.whois.whois", return_value=fake_whois):
        dias = verificar_idade_dominio("https://exemplo.com")
    assert 499 <= dias <= 500


def test_verificar_idade_dominio_lista_usa_primeira_data():
    criado_em = datetime.now() - timedelta(days=100)
    fake_whois = mock.Mock(creation_date=[criado_em, criado_em - timedelta(days=1000)])
    with mock.patch("termometro.security_checks.whois.whois", return_value=fake_whois):
        dias = verificar_idade_dominio("https://exemplo.com")
    assert 99 <= dias <= 100


def test_verificar_idade_dominio_sem_data_retorna_invalido():
    fake_whois = mock.Mock(creation_date=None)
    with mock.patch("termometro.security_checks.whois.whois", return_value=fake_whois):
        assert verificar_idade_dominio("https://exemplo.com") == -1


def test_verificar_idade_dominio_consulta_falha_retorna_invalido():
    with mock.patch("termometro.security_checks.whois.whois", side_effect=Exception("timeout")):
        assert verificar_idade_dominio("https://exemplo.com") == -1


def test_google_safe_browsing_detecta_match():
    fake_response = mock.Mock()
    fake_response.json.return_value = {"matches": [{"threatType": "MALWARE"}]}
    with mock.patch("termometro.security_checks.requests.post", return_value=fake_response):
        assert consultar_google_safe_browsing("https://golpe.example") is True


def test_google_safe_browsing_sem_match():
    fake_response = mock.Mock()
    fake_response.json.return_value = {}
    with mock.patch("termometro.security_checks.requests.post", return_value=fake_response):
        assert consultar_google_safe_browsing("https://seguro.example") is False


def test_google_safe_browsing_falha_de_rede_nao_quebra():
    import requests

    with mock.patch("termometro.security_checks.requests.post", side_effect=requests.RequestException):
        assert consultar_google_safe_browsing("https://exemplo.com") is False
