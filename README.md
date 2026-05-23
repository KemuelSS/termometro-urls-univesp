# 🛡️ Termômetro de Confiança de URLs

![Status](https://img.shields.io/badge/Status-Concluido-success)
![Versão](https://img.shields.io/badge/Versão-2.0%20(Dark%20Premium)-blue)
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

## ✨ Evoluções e Melhorias da Versão 2.0 (Premium Update)
A nova versão trouxe uma reformulação completa focada em padrões profissionais de mercado, combinando design de alta autoridade, otimização de infraestrutura e experiência do usuário (UX):

* **Interface Dark Mode Premium:** Transição visual completa para uma paleta monocromática baseada em tons de *Slate* com efeito *Glassmorphism* escuro (textura de vidro jateado translúcido e desfoque via CSS). O visual foi projetado para simular painéis de segurança corporativos, destacando de forma cirúrgica as cores dos alertas de score.
* **Microinterações e Focus State:** Implementação de transições suaves e feedbacks visuais em tempo real. Campos de formulário agora contam com uma "aura" de brilho azul responsiva ao clique do usuário (*focus*), e os botões de ação utilizam efeitos sutis de elevação (*hover*).
* **Responsividade Mobile Completa:** Refatoração do layout através de Media Queries estruturadas, garantindo que o sistema se adapte de forma nativa a smartphones.
* **Transparência e Segurança no Mobile:** Implementação estratégica de quebras de linha (`word-break: break-all`) que forçam a renderização integral de links extensos ou mascarados no histórico de consultas, impedindo o corte visual do CSS e mantendo a transparência total no mobile.
* **Branding e Compartilhamento Profissional:** Integração de Favicon dinâmico acoplado às rotas do Flask para eliminar erros de carregamento e inserção de metadados robustos (Open Graph), permitindo que o link gere cards informativos padronizados ao ser compartilhado em redes sociais e aplicativos de mensagem.
* **Persistência Autogerenciável:** Configuração do banco de dados SQLite3 para se auto-inicializar dinamicamente a cada requisição no ambiente de produção (Gunicorn/Render).
* **Isolamento de Credenciais:** Uso de variáveis de ambiente seguras (`os.getenv`) para ocultar e proteger a chave privada de API do Google do repositório público do GitHub.

## 🛠️ Tecnologias Utilizadas
* **Back-end:** Python, Flask, `gunicorn`, `requests`, `python-whois`, `socket`, `python-dotenv`.
* **Banco de Dados:** SQLite3 (Histórico local de consultas recentes com exibição dinâmica).
* **Front-end:** HTML5 semântico, CSS3 avançado (Flexbox avançado, Glassmorphism, Focus States e Responsividade), JavaScript nativo para gerenciamento de loaders e animações assíncronas.

## 👥 Autores e Papéis (Grupo PI - Univesp)

* **Kemuel dos Santos Sousa** - *Product Owner / QA / UI-UX* (Liderança do produto, garantia de qualidade do código, engenharia de front-end responsivo e design de interface).
  
* **Karoline Thaiane Cumim** - *Technical Writer & UX Researcher* (Documentação técnica, elaboração dos relatórios acadêmicos oficiais e estruturação da coleta de feedbacks).
  
* **Kelvin Souza Cardoso da Costa** - *Tech Lead & Cloud/DevOps* (Definição da stack tecnológica, desenvolvimento da arquitetura de software e estratégia de deploy ágil).

---
*Projeto desenvolvido para fins acadêmicos - Universidade Virtual do Estado de São Paulo (Univesp)*
