from dotenv import load_dotenv
import os
import requests
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import whois
from urllib.parse import urlparse
import socket

app = Flask(__name__)
# Chave da API Safe Browsing do Google
GOOGLE_API_KEY = "AIzaSyAQimygIcpsrLQzChekBmopzNJDersNVs4" 

# --- Funções do Banco de Dados ---
def get_db_connection():
    conn = sqlite3.connect('banco_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            trust_score INTEGER,
            data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    init_db()

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
        
        # 1. Busca o IP
        try:
            dominio_limpo = extrair_dominio(url)
            ip_site = socket.gethostbyname(dominio_limpo)
        except:
            ip_site = "IP Indisponível"

        # 2. Executa as checagens (API Google + WHOIS)
        e_golpe_confirmado = consultar_google_safe_browsing(url)
        dias_de_vida = verificar_idade_dominio(url)

        # 3. Motor de Regras (Prioridade: Se o Google diz que é golpe, o score é 0)
        if e_golpe_confirmado:
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

        # 4. Salva no banco de dados apenas UMA vez
        conn = get_db_connection()
        conn.execute('INSERT INTO consultas (url, trust_score) VALUES (?, ?)', (url, trust_score))
        conn.commit()
        conn.close()

    # 5. Carrega o histórico (Sempre fora do IF POST)
    conn = get_db_connection()
    historico_db = conn.execute('SELECT url, trust_score FROM consultas ORDER BY id DESC LIMIT 5').fetchall()
    conn.close()

    return render_template('index.html', resultado=resultado, url_analisada=url_analisada, historico=historico_db, ip_site=ip_site)

if __name__ == '__main__':
    app.run(debug=True)