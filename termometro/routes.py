import logging

from flask import Blueprint, current_app, render_template, request, send_from_directory

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

    historico_db = listar_historico()
    return render_template(
        'index.html',
        resultado=resultado,
        url_analisada=url_analisada,
        historico=historico_db,
        ip_site=ip_site,
    )
