# 🛡️ Termômetro de Confiança de URLs

![Status](https://img.shields.io/badge/Status-Concluido-success)
![Versão](https://img.shields.io/badge/Versão-2.1%20(Procon%20Update)-blue)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)

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

## ✨ Evoluções e Melhorias da Versão 2.1 (Premium & Procon Update)
A nova versão trouxe uma reformulação completa focada em padrões profissionais de mercado, combinando design de alta autoridade, otimização de infraestrutura e experiência do usuário (UX):

* **Inteligência de Ameaças Regional:** Implementação nativa da lista de sites a evitar do Procon-SP, cobrindo uma falha comum em APIs globais (que focam em vírus, mas deixam passar golpes comerciais brasileiros).
* **Interface Dark Mode Premium:** Transição visual completa para uma paleta monocromática baseada em tons de *Slate* com efeito *Glassmorphism* escuro, projetado para simular painéis de segurança corporativos e destacar as cores dos alertas.
* **Microinterações e Focus State:** Feedbacks visuais em tempo real. Campos contam com uma "aura" de brilho responsiva ao clique (*focus*), e botões utilizam efeitos de elevação (*hover*).
* **Responsividade Mobile Completa:** Refatoração através de Media Queries, garantindo adaptação nativa a smartphones.
* **Transparência e Segurança no Mobile:** Implementação de quebras de linha (`word-break: break-all`) que forçam a renderização integral de links extensos no histórico, impedindo o mascaramento visual no celular.
* **Branding e Compartilhamento Profissional:** Integração de Favicon dinâmico e metadados (Open Graph) para geração de cards informativos em redes sociais.
* **Isolamento de Credenciais:** Uso de variáveis de ambiente seguras (`os.getenv`) para ocultar a chave privada de API do Google.

## 🛠️ Tecnologias Utilizadas
* **Back-end:** Python, Flask, `gunicorn`, `requests`, `python-whois`, `socket`, `python-dotenv`.
* **Banco de Dados:** SQLite3 (Histórico local de consultas recentes com exibição dinâmica).
* **Front-end:** HTML5 semântico, CSS3 avançado (Flexbox, Glassmorphism, Responsividade), JavaScript nativo.

## 👥 Autores e Papéis (Grupo PI - Univesp)

* **Kemuel dos Santos Sousa** - *Product Owner / QA / UI-UX* (Liderança do produto, garantia de qualidade, engenharia de front-end responsivo e design de interface).
  
* **Karoline Thaiane Cumim** - *Technical Writer & UX Researcher* (Documentação técnica, elaboração dos relatórios acadêmicos oficiais e estruturação da coleta de feedbacks).
  
* **Kelvin Souza Cardoso da Costa** - *Tech Lead & Cloud/DevOps* (Definição da stack tecnológica, desenvolvimento da arquitetura de software tripla e estratégia de deploy ágil).

---
*Projeto desenvolvido para fins acadêmicos - Universidade Virtual do Estado de São Paulo (Univesp)*