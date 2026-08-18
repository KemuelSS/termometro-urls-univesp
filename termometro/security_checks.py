import ipaddress
import logging
import socket
from datetime import datetime
from urllib.parse import urlparse

import requests
import whois

from .config import GOOGLE_API_KEY

logger = logging.getLogger(__name__)

GOOGLE_SAFE_BROWSING_TIMEOUT = 5
WHOIS_TIMEOUT = 5


def extrair_dominio(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    domain = domain.replace('www.', '')
    return domain.split('/')[0]


def resolver_ip(dominio):
    """Resolve o IP do domínio.

    Retorna None se o domínio não resolver ou se resolver para um
    endereço privado/loopback/reservado: nesses casos o domínio é
    tratado como inválido em vez de exibir um IP interno para o
    usuário, o que também fecha a porta pra abuso caso a ferramenta
    passe a buscar conteúdo do domínio no futuro.
    """
    try:
        ip = socket.gethostbyname(dominio)
    except socket.gaierror:
        return None

    endereco = ipaddress.ip_address(ip)
    if endereco.is_private or endereco.is_loopback or endereco.is_link_local or endereco.is_reserved:
        logger.warning("Domínio %r resolveu para endereço não-público (%s), tratando como inválido.", dominio, ip)
        return None

    return ip


def verificar_idade_dominio(url):
    dominio_limpo = extrair_dominio(url)
    try:
        dominio_info = whois.whois(dominio_limpo, timeout=WHOIS_TIMEOUT)
    except Exception:
        logger.info("Consulta WHOIS falhou para %r.", dominio_limpo, exc_info=True)
        return -1

    data_criacao = dominio_info.creation_date
    if isinstance(data_criacao, list):
        data_criacao = data_criacao[0]

    if not data_criacao:
        return -1

    data_criacao = data_criacao.replace(tzinfo=None)
    return (datetime.now() - data_criacao).days


def consultar_google_safe_browsing(url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    payload = {
        "client": {"clientId": "termometro-url", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    try:
        response = requests.post(api_url, json=payload, timeout=GOOGLE_SAFE_BROWSING_TIMEOUT)
        data = response.json()
    except (requests.RequestException, ValueError):
        logger.warning("Consulta ao Google Safe Browsing falhou para %r.", url, exc_info=True)
        return False

    return "matches" in data
