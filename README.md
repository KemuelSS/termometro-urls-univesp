# 🛡️ Termômetro de Confiança de URLs

![Status](https://img.shields.io/badge/Status-Concluido-success)
![Versão](https://img.shields.io/badge/Versão-3.0%20(PI2)-blue)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)
![Testes](https://github.com/KemuelSS/termometro-urls-univesp/actions/workflows/tests.yml/badge.svg)

Um sistema web desenvolvido em Python (Flask) para analisar links suspeitos e alertar os usuários sobre possíveis riscos de fraude, phishing e malware. Este projeto faz parte do escopo acadêmico do **Projeto Integrador - Univesp**.

## 🌐 Demonstração Online (Deploy)
A aplicação está totalmente hospedada na nuvem e pode ser acessada em tempo real por qualquer dispositivo (computador ou smartphone) através do link abaixo:

🔗 **[Acessar o Termômetro de URLs](https://termometro-urls-univesp.onrender.com)**

---

## 🚀 O Problema e a Solução
Com o aumento de golpes digitais (como falsas cobranças de pedágio via SMS e promoções fraudulentas), usuários leigos têm dificuldade em identificar links maliciosos. O Termômetro de URLs atua como uma ferramenta de **segurança preventiva**, analisando a reputação e a procedência do link antes que o usuário clique ou insira dados sensíveis.

## 🧠 Arquitetura de Defesa em Três Camadas
O sistema utiliza um motor de regras inteligente que cruza dados de três fontes distintas para gerar um **Trust Score (0 a 100)**:

1. **Camada Zero: Threat Intelligence Local (Procon-SP)**
   - Validação instantânea (O(1)) do domínio contra a lista oficial de bloqueio do Procon-SP (sites com histórico de fraudes comerciais e não entrega de produtos).
   - *Se detectado:* Score 0 com alerta exclusivo, economizando tempo e requisições de API.

2. **Camada Um: Google Safe Browsing API (Reputação Global)**
   - Consulta a URL contra a lista negra oficial e atualizada do Google (Malware, Engenharia Social, Software Indesejado).
   - *Se detectado:* Score 0 (Perigo Crítico).

3. **Camada Dois: WHOIS Data (Análise de Ameaças Zero-Day)**
   - Para links que escapam das duas primeiras listas, o sistema extrai o domínio e consulta a data de criação do servidor.
   - Domínios recém-criados recebem pontuações baixas (**Alto Risco**), mitigando golpes que acabaram de nascer.

## ✨ Evolução da Plataforma

### PI2 — Núcleo do Edital e Diferenciais (Versão 3.0)
Segunda fase do projeto, focada em consolidar os requisitos técnicos do edital e agregar diferenciais analíticos à plataforma:

* **Score Contínuo e Ponderado:** o motor de regras deixou de usar 5 valores fixos de score e passou a calcular uma nota de 0 a 100, combinando de forma ponderada a idade do domínio (WHOIS) e a validade da resolução de IP. Sinais de lista negra confirmada (Procon-SP e Google Safe Browsing) continuam resultando em bloqueio imediato.
* **Explicabilidade do Score:** cada resultado traz o detalhamento de quais fatores formaram a nota e o peso de cada um, visível diretamente na interface.
* **Dashboard de Análise de Dados:** página nova (`/dashboard`) com estatísticas agregadas do histórico de consultas — distribuição de scores por faixa de risco, domínios mais consultados e taxa de detecção por fonte.
* **Interface Dinâmica (JavaScript sem reload):** o formulário de consulta atualiza o resultado via fetch/AJAX, sem recarregar a página, mantendo compatibilidade com navegadores sem suporte a JavaScript.
* **Acessibilidade:** rótulo associado ao campo de URL, regiões de leitura dinâmica (`aria-live`) para leitores de tela anunciarem atualizações automaticamente, e estado de carregamento acessível.
* **Persistência em PostgreSQL:** migração da camada de dados do SQLite local para uma instância gerenciada de PostgreSQL via SQLAlchemy ORM, resolvendo a perda do histórico de consultas a cada novo deploy no ambiente de hospedagem.
* **Testes Automatizados e Integração Contínua:** suíte de testes com pytest cobrindo o motor de score, as verificações de segurança e as rotas da aplicação, executada automaticamente a cada push via GitHub Actions.

### PI1 — Versão 2.1 (Premium & Procon Update)
Primeira evolução da plataforma, focada em padrões profissionais de mercado, combinando design de alta autoridade, otimização de infraestrutura e experiência do usuário (UX):

* **Inteligência de Ameaças Regional:** Implementação nativa da lista de sites a evitar do Procon-SP, cobrindo uma falha comum em APIs globais (que focam em vírus, mas deixam passar golpes comerciais brasileiros).
* **Interface Dark Mode Premium:** Transição visual completa para uma paleta monocromática baseada em tons de *Slate* com efeito *Glassmorphism* escuro, projetado para simular painéis de segurança corporativos e destacar as cores dos alertas.
* **Microinterações e Focus State:** Feedbacks visuais em tempo real. Campos contam com uma "aura" de brilho responsiva ao clique (*focus*), e botões utilizam efeitos de elevação (*hover*).
* **Responsividade Mobile Completa:** Refatoração através de Media Queries, garantindo adaptação nativa a smartphones.
* **Transparência e Segurança no Mobile:** URLs extensas no histórico quebram de forma legível em telas pequenas (`overflow-wrap: anywhere`), sem cortar no meio da palavra, evitando mascaramento visual no celular.
* **Branding e Compartilhamento Profissional:** Integração de Favicon dinâmico e metadados (Open Graph) para geração de cards informativos em redes sociais.
* **Isolamento de Credenciais:** Uso de variáveis de ambiente seguras (`os.getenv`) para ocultar a chave privada de API do Google.

## 🛠️ Tecnologias Utilizadas
* **Back-end:** Python, Flask, `gunicorn`, `requests`, `python-whois`, `socket`, `python-dotenv`.
* **Banco de Dados:** PostgreSQL em produção via SQLAlchemy ORM, com fallback automático para SQLite em desenvolvimento local.
* **Front-end:** HTML5 semântico, CSS3 avançado (Flexbox, Glassmorphism, Responsividade), JavaScript nativo (fetch/AJAX, sem reload de página).
* **Testes:** pytest (testes automatizados do motor de score, verificações de segurança e rotas).
* **CI:** GitHub Actions rodando a suíte de testes a cada push.

## 💻 Rodando o projeto localmente

**Pré-requisitos:** Python 3.11 ou superior.

```bash
# Clone o repositório
git clone https://github.com/KemuelSS/termometro-urls-univesp.git
cd termometro-urls-univesp

# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# edite o .env e preencha GOOGLE_API_KEY (DATABASE_URL é opcional — sem ela, usa SQLite local)

# Rode a aplicação
python app.py
```

A aplicação sobe em `http://localhost:5000`.

### Rodando os testes

```bash
pip install -r requirements-dev.txt
pytest
```

## 👥 Autores e Papéis (Grupo PI - Univesp)

Grupo formado a partir do PI1 e ampliado para 8 integrantes no PI2:

* **Ana Cláudia de Paula Fontanezi** - *Redação e Documentação Acadêmica* (Elaboração do Plano de Ação e apoio na redação dos relatórios oficiais).

* **Camila dos Santos Cruz** - *Pesquisa e Redação* (Pesquisas e textos de apoio aos relatórios acadêmicos).

* **Daniel Segundo de Carvalho** - *Apoio ao Projeto*.

* **Eliesel de Melo Tanada** - *Design e Apresentação* (Material visual, roteiro e produção do vídeo final de apresentação).

* **Karoline Thaiane Cumim** - *Technical Writer & UX Researcher* (Documentação técnica, elaboração dos relatórios acadêmicos oficiais e estruturação da coleta de feedbacks).

* **Kathelyn Vitoria Pergentino Reis Anastacio** - *Análise de Dados* (Interpretação dos dados coletados pela plataforma).

* **Kelvin Souza Cardoso da Costa** - *Tech Lead & Cloud/DevOps* (Definição da stack tecnológica, desenvolvimento da arquitetura de software tripla e estratégia de deploy ágil).

* **Kemuel dos Santos Sousa** - *Product Owner / QA / UI-UX* (Liderança do produto, garantia de qualidade, engenharia de front-end responsivo e design de interface).

---
*Projeto desenvolvido para fins acadêmicos - Universidade Virtual do Estado de São Paulo (Univesp)*