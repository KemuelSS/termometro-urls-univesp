# 🛡️ Termômetro de Confiança de URLs

![Status](https://img.shields.io/badge/Status-Concluido-success)
![Versão](https://img.shields.io/badge/Versão-2.0%20(Responsiva)-blue)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)

Um sistema web desenvolvido em Python (Flask) para analisar links suspeitos e alertar os usuários sobre possíveis riscos de fraude, phishing e malware. Este projeto faz parte do escopo acadêmico do **Projeto Integrador - Univesp**.

## 🌐 Demonstração Online (Deploy)
A aplicação está totalmente hospedada na nuvem e pode ser acessada em tempo real por qualquer dispositivo (computador ou smartphone) através do link abaixo:

🔗 **[Acessar o Termômetro de URLs](https://termometro-urls-univesp.onrender.com)**

---

## 🚀 O Problema e a Solução
Com o aumento de golpes digitais (como falsas cobranças de pedágio via SMS e promoções fraudulentas), usuários leigos têm dificuldade em identificar links maliciosos. O Termômetro de URLs atua como uma ferramenta de **segurança preventiva**, analisando a reputação e a procedência do link antes que o usuário clique ou insira dados sensíveis.

## 🧠 Arquitetura de Defesa em Duas Camadas
O sistema utiliza um motor de regras que cruza dados de duas fontes distintas para gerar um **Trust Score (0 a 100)**:

1. **Google Safe Browsing API (Reputação em Tempo Real):**
   - Consulta a URL contra a lista negra oficial do Google (Malware, Engenharia Social, Software Indesejado).
   - *Se detectado:* O Score cai imediatamente para **0 (Perigo Crítico)**, sobrepondo qualquer outra métrica.

2. **WHOIS Data (Análise Temporal e de Infraestrutura):**
   - Para links que ainda não estão na base do Google (ameaças *Zero-Day*), o sistema extrai o domínio e consulta a data de registro do servidor.
   - Domínios criados há poucos dias recebem pontuações baixas (**Risco Alto**).
   - Domínios antigos e estabelecidos recebem pontuações altas (**Seguro**).

## ✨ Novidades da Versão 2.0
* **Responsividade Mobile:** Refatoração completa do CSS com Media Queries para adaptação perfeita em smartphones.
* **Leitura Integral de URLs:** Implementação de `word-break` estratégico no front-end para impedir o corte de links longos e maliciosos, garantindo transparência total ao usuário mobile no histórico de consultas.
* **Persistência Autogerenciável:** Configuração do banco de dados SQLite3 para se auto-inicializar dinamicamente a cada requisição no ambiente de produção (Gunicorn/Render).
* **Isolamento de Credenciais:** Uso de variáveis de ambiente seguras para ocultar a chave de API do Google do repositório público.

## 🛠️ Tecnologias Utilizadas
* **Back-end:** Python, Flask, `gunicorn`, `requests`, `python-whois`, `socket`.
* **Banco de Dados:** SQLite3 (Histórico local de consultas recentes).
* **Front-end:** HTML5, CSS3 avançado (Interface limpa com foco em alertas visuais de risco).

## 👥 Autores e Papéis (Grupo PI - Univesp)

* **Kemuel dos Santos Sousa** * *Product Owner / QA / UI-UX* (Liderança do produto, garantia de qualidade, testes responsivos e design de interface).
  
* **Karoline Thaiane Cumim** * *Technical Writer & UX Researcher* (Documentação técnica, elaboração dos relatórios oficiais e estruturação da coleta de feedbacks).
  
* **Kelvin Souza Cardoso da Costa** * *Tech Lead & Cloud/DevOps* (Definição da stack tecnológica, arquitetura de software e estratégia de deploy ágil via Replit para validação).

---
*Projeto desenvolvido para fins acadêmicos - Universidade Virtual do Estado de São Paulo (Univesp)*
