from dotenv import load_dotenv
import os
import requests
from flask import Flask, render_template, request, send_from_directory 
import sqlite3
from datetime import datetime
import whois
from urllib.parse import urlparse
import socket

load_dotenv()

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'escudo.png', mimetype='image/png')

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- LISTA DE BLOQUEIO LOCAL (PROCON-SP) ---
# Atualizada em Maio/2026
PROCON_BLOCKLIST = {
    "123importados.com",
    "123multiofertas.com.br",
    "123multiofertas.net",
    "acessivelmodasbras.com.br",
    "agachecomercial.net",
    "allprinter.com.br",
    "ascarishop.com",
    "bmjbaby.com.br",
    "boavistaacabamentos.com",
    "boticamaviris.com.br",
    "brasilmagazine.com",
    "brezzy.com.br",
    "caixamisteriosa.com",
    "casadonatebrasil.com",
    "casakith.com.br",
    "casamagazinebrasil.com",
    "centroofertas.com.br",
    "cintosbyhi.com.br",
    "cogumeloshop.com",
    "comandantedasofertas.com",
    "compufree.com.br",
    "dbellestore.com",
    "descontosbrasileiro.com",
    "drogariamc.com.br",
    "dutrametais.com",
    "equipamentosrodrigues.com",
    "everestgroup.com.br",
    "fabricaauthenticite.com",
    "fabricashoes.com.br",
    "feme.com.br",
    "ferrutini.com.br",
    "flystorebrasil.com.br",
    "fully.com.br",
    "futcertobrasil.com",
    "gelniche.com.br",
    "gigavarejo.com.br",
    "gomic.com.br",
    "hofferta.com",
    "hotelurbano.com.br",
    "hurb.com",
    "iluminim.com.br",
    "iwoseries.com",
    "laserfast.com",
    "lbashop.com.br",
    "leggingbrasil.com",
    "leggingbrasil.com.br",
    "lewadoimports.com",
    "liquidashoes.com.br",
    "lojaatlantis.com",
    "lojabestvarejos.com",
    "lojacondi.com",
    "lojadigivarejista.com",
    "lojadubaiimports.com.br",
    "lojamiofarma.com",
    "lojaslondrina.com.br",
    "lojavitesse.com",
    "lovelybox.com.br",
    "magazineal.com",
    "magazinedosatacados.com",
    "magazinestore.com",
    "magazinmulher.com.br",
    "marabraz.com.br",
    "mundialeletro.com.br",
    "nuvemdedescontos.com",
    "ofertastore.com",
    "outletdasfraldas.com.br",
    "peixeurbano.com.br",
    "premierexclusive.com.br",
    "rocklin.com.br",
    "rosafashion.com.br",
    "safiravillage.com.br",
    "saldaocarioca.com.br",
    "santolarmoveis.com.br",
    "shopmaxx.com.br",
    "sigaofertas.com.br",
    "tecnotec.com.br",
    "tiggoshop.com.br",
    "usenox.com",
    "vivadecor.com.br",
    "vivonestore.com",
    "zinnimodas.com"
}

# --- Funções do Banco de Dados ---
def get_db_connection():
    conn = sqlite3.connect('banco_dados.db')
    conn.row_factory = sqlite3.Row
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            trust_score INTEGER,
            data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    return conn

# --- Lógica de Segurança (Heurísticas) ---
def extrair_dominio(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    domain = domain.replace('www.', '')
    return domain

def verificar_idade_dominio(url):
    try:
        dominio_limpo = extrair_dominio(url)
        print(f"\n[LOG] Consultando WHOIS para: {dominio_limpo}")
        
        dominio_info = whois.whois(dominio_limpo)
        data_criacao = dominio_info.creation_date
        
        if isinstance(data_criacao, list):
            data_criacao = data_criacao[0]
            
        if data_criacao:
            data_criacao = data_criacao.replace(tzinfo=None)
            dias_de_vida = (datetime.now() - data_criacao).days
            return dias_de_vida
        return -1 
    except Exception as e:
        print(f"[LOG] Erro WHOIS: {e}")
        return -1

def consultar_google_safe_browsing(url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    payload = {
        "client": {"clientId": "termometro-url", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(api_url, json=payload, timeout=5)
        data = response.json()
        return "matches" in data
    except Exception as e:
        print(f"[LOG] Erro API Google: {e}")
        return False

# --- Rota Principal ---
@app.route('/', methods=('GET', 'POST'))
def index():
    resultado = None
    url_analisada = None
    ip_site = None

    if request.method == 'POST':
        url = request.form['url']
        url_analisada = url

        # 1. Garante a extração limpa do domínio de forma blindada
        try:
            dominio_limpo = extrair_dominio(url)
        except:
            # Fallback caso a função falhe ou o usuário digite algo estranho
            dominio_limpo = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]

        # 2. Busca o IP com base no domínio que já temos garantido
        try:
            ip_site = socket.gethostbyname(dominio_limpo)
        except:
            ip_site = "IP Indisponível"

        # 3. Executa as checagens (PROCON > API Google > WHOIS)
        na_lista_procon = dominio_limpo.lower() in PROCON_BLOCKLIST

        if na_lista_procon:
            e_golpe_confirmado = False
            dias_de_vida = 0
        else:
            e_golpe_confirmado = consultar_google_safe_browsing(url)
            dias_de_vida = verificar_idade_dominio(url)

        # 4. Motor de Regras (Prioridade: Procon > Google > WHOIS)
        if na_lista_procon:
            trust_score = 0
            status = "🚨 ALERTA PROCON-SP: Este site consta na lista oficial de sites a evitar (Fraude/Não entrega)."
            cor = "res-red"
        elif e_golpe_confirmado:
            trust_score = 0
            status = "PERIGO CRÍTICO: Este link está na lista negra de fraudes do Google!"
            cor = "res-red"
        elif dias_de_vida == -1:
            trust_score = 10
            status = "Perigo: Domínio inválido, oculto ou suspeito."
            cor = "res-red"
        elif dias_de_vida < 30:
            trust_score = 30
            status = f"Perigo: Site muito recente ({dias_de_vida} dias). Alto risco."
            cor = "res-red"
        elif dias_de_vida < 180:
            trust_score = 60
            status = f"Atenção: Site relativamente novo ({dias_de_vida} dias)."
            cor = "res-orange"
        else:
            trust_score = 95
            status = f"Seguro: Site estabelecido e antigo ({dias_de_vida} dias)."
            cor = "res-green"

        resultado = {"score": trust_score, "status": status, "cor": cor}

        # 5. Salva no banco de dados apenas UMA vez
        conn = get_db_connection()
        conn.execute('INSERT INTO consultas (url, trust_score) VALUES (?, ?)', (url, trust_score))
        conn.commit()
        conn.close()

    # 6. Carrega o histórico (Sempre fora do IF POST para aparecer ao abrir a página)
    conn = get_db_connection()
    historico_db = conn.execute('SELECT url, trust_score FROM consultas ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()

    return render_template('index.html', resultado=resultado, url_analisada=url_analisada, historico=historico_db, ip_site=ip_site)

if __name__ == '__main__':
    app.run(debug=True)