import logging

from flask import Blueprint, current_app, jsonify, render_template, request, send_from_directory

from .blocklist import PROCON_BLOCKLIST
from .db import listar_historico, salvar_consulta
from .scoring import calcular_resultado
from .security_checks import (
    consultar_google_safe_browsing,
    extrair_dominio,
    resolver_ip,
    verificar_idade_dominio,
)

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)


def analisar_url(url):
    """Roda a triangulação de segurança (Procon > Google Safe Browsing > WHOIS)
    pra uma URL e já salva a consulta no histórico. Usado tanto pela rota
    com reload (fallback sem JS) quanto pelo endpoint JSON do fetch."""
    try:
        dominio_limpo = extrair_dominio(url)
    except ValueError:
        logger.warning("Falha ao extrair domínio de %r, usando fallback.", url)
        dominio_limpo = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]

    ip_site = resolver_ip(dominio_limpo) or "IP Indisponível"

    na_lista_procon = dominio_limpo.lower() in PROCON_BLOCKLIST

    if na_lista_procon:
        golpe_confirmado = False
        dias_de_vida = 0
    else:
        golpe_confirmado = consultar_google_safe_browsing(url)
        dias_de_vida = verificar_idade_dominio(url)

    resultado = calcular_resultado(na_lista_procon, golpe_confirmado, dias_de_vida)
    salvar_consulta(url, resultado["score"])
    return resultado, ip_site


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'escudo.png', mimetype='image/png')


@bp.route('/', methods=('GET', 'POST'))
def index():
    resultado = None
    url_analisada = None
    ip_site = None

    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        if url:
            url_analisada = url
            resultado, ip_site = analisar_url(url)

    historico_db = listar_historico()
    return render_template(
        'index.html',
        resultado=resultado,
        url_analisada=url_analisada,
        historico=historico_db,
        ip_site=ip_site,
    )


@bp.route('/api/analisar', methods=('POST',))
def analisar_json():
    """Mesma análise da rota principal, mas sem recarregar a página: usada
    pelo static/app.js via fetch. Se o JS estiver desabilitado, o form
    continua funcionando normalmente pela rota '/' acima."""
    url = request.form.get('url', '').strip()
    if not url:
        return jsonify(erro="URL em branco."), 400

    resultado, ip_site = analisar_url(url)
    historico_db = listar_historico()

    return jsonify(
        resultado=resultado,
        ip_site=ip_site,
        url_analisada=url,
        historico=[
            {"url": item["url"], "trust_score": item["trust_score"]}
            for item in historico_db
        ],
    )
