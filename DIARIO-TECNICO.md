# 📓 Diário Técnico — Termômetro de URLs (PI2)

Este documento registra, em ordem cronológica, as decisões e o trabalho técnico feito no projeto durante o PI2 (2026.2). Ele existe pra separar duas coisas que não deveriam depender uma da outra: o código evolui no repositório, mas quem escreve o relatório não precisa ler código nem histórico de commits pra saber o que foi feito e por quê.

**Como usar isto**: cada entrada abaixo tem contexto, o que foi feito, por que e como foi validado. Não é texto pronto pra colar no relatório (o tom aqui é técnico e direto), mas é a matéria-prima: as seções de metodologia e resultados do Plano de Ação, do Relatório Parcial e do Relatório Final podem ser escritas em cima disso, do jeito que o PI1 já fez com as etapas "ouvir e interpretar / criar e prototipar / implementar e testar". Cada entrada é marcada com a fase e a quinzena do [cronograma oficial](https://claude.ai/code/artifact/4e7517a7-a996-4029-9bda-37b703459562) a que pertence.

Trilha técnica: Kemuel Sousa, com apoio do Claude (Anthropic). Dúvidas sobre qualquer entrada, chamar o Kemuel.

---

## Decisão de continuar o projeto

**Quando**: antes da Quinzena 1 (10/08/2026).

**Contexto**: o PI2 reuniu um grupo maior (8 pessoas) a partir dos três autores do PI1 (Karoline Cumim, Kelvin Costa, Kemuel Sousa). O edital deste semestre pede: framework web, banco de dados, script web (JavaScript), nuvem, uso de API, acessibilidade, controle de versão e testes, com análise de dados como item opcional.

**Decisão**: em vez de começar um projeto novo, o grupo optou por continuar e evoluir o Termômetro de URLs, o sistema entregue no PI1. Motivos: o sistema já está em produção e testável ao vivo; já existe pesquisa de campo com 54 participantes da comunidade (dado citado no relatório do PI1); e, cruzando com o edital deste semestre, 4 dos 8 requisitos obrigatórios já estavam resolvidos sem escrever uma linha de código nova (framework web, nuvem, uso de API, controle de versão).

**Divisão de trabalho**: Kemuel Sousa ficou responsável pela trilha técnica (código, testes, deploy) trabalhando com apoio de IA (Claude). O restante do grupo, incluindo Karoline e Kelvin, cuida da redação do relatório, fundamentação teórica, coleta de feedback com a comunidade e apresentação/vídeo final.

**Opcional assumido**: o grupo decidiu entregar também o item opcional do edital (análise de dados), já que o histórico de consultas do sistema já é matéria-prima suficiente para um dashboard, e o custo extra é baixo.

---

## Reavaliação da stack tecnológica

**Quando**: antes da Quinzena 1 (10/08/2026).

**Contexto**: o sistema original foi construído com pouco conhecimento técnico acumulado pela equipe na época. Antes de continuar em cima dele, avaliamos se as escolhas de linguagem, framework, banco de dados e hospedagem ainda faziam sentido, ou se valeria migrar para outra stack.

**Decisão, camada por camada**:
- **Linguagem e framework (Python + Flask)**: mantido. Curva de aprendizado mais suave para um grupo de 8 pessoas com níveis técnicos mistos, e já resolve o requisito de framework web do edital. Reescrever em outra linguagem ou framework não destravaria nenhum requisito novo.
- **Banco de dados (SQLite)**: será substituído por Postgres gerenciado + SQLAlchemy na Fase 2. O SQLite puro tinha um problema real: como o Render (plataforma de hospedagem) não mantém disco persistente no plano gratuito, o histórico de consultas era apagado a cada novo deploy.
- **Hospedagem (Render)**: mantida. O problema nunca foi a plataforma, era a ausência de banco persistente — resolvido ativando o Postgres gerenciado do próprio Render, sem o custo de aprender infraestrutura nova (AWS/GCP) dentro do prazo do semestre.
- **Frontend (HTML/CSS + JavaScript puro)**: mantido, sem introduzir um framework de frontend (React, Vue). JavaScript puro já é suficiente para cumprir o requisito de script web do edital.

---

## Divisão de papéis no grupo

**Quando**: a partir da Quinzena 1 (10/08/2026), em atualização contínua conforme o grupo maior (8 pessoas) responde no WhatsApp.

**Contexto**: além da trilha técnica (Kemuel), o grupo definiu outras frentes de trabalho: entrega dos documentos na plataforma (AVA), escrita/redação, coleta de feedback com a comunidade externa, análise de dados (pesquisa + dashboard), vídeo de apresentação e outras funções/atividades necessárias. Cada pessoa foi convidada a indicar o que prefere fazer.

**Quem já se posicionou**:

| Nome | Frente |
|---|---|
| Camila | Textos e pesquisas (avisou que ainda não tem familiaridade com código) |
| Tanada | Design e apresentação — interface, material visual, roteiro e produção do vídeo final (tem experiência com Design Gráfico) |
| Ana Claudia | Textos — se ofereceu pra esboçar o Plano de Ação e enviar pro grupo avaliar |
| Kathelyn | Análise de dados (avisou que também ajuda no que mais precisar) |
| Karoline | Entrega dos relatórios e materiais na plataforma (AVA) |
| Kelvin | Apoio geral, no que for necessário |

**Daniel** chegou a demonstrar interesse em ajudar na parte técnica (migração do banco de dados), mas não retornou contato depois disso. A trilha técnica segue só com Kemuel + Claude.

*Tabela em aberto — atualizar conforme mais respostas chegarem no grupo.*

---

## Fase 1 — Fundação e dívida técnica

**Quando**: concluída em 08/08/2026 (Quinzenas 1–2, janela 10/08–06/09).

**Contexto**: antes de implementar qualquer funcionalidade nova exigida pelo edital, o código precisava sair do estado de MVP acadêmico (tudo em um único arquivo, sem tratamento de erro consistente) para um estado que suportasse testes automatizados e mudanças futuras com segurança.

**O que foi feito**:
1. **Reorganização do código**: o arquivo único `app.py` (247 linhas, misturando rotas, regras de negócio e acesso a dados) foi dividido em um pacote `termometro/` com responsabilidades separadas: configuração, lista de bloqueio do Procon-SP, verificações de segurança (Google Safe Browsing, WHOIS, resolução de IP), motor de cálculo do score, acesso ao banco de dados, e as rotas Flask propriamente ditas. `app.py` passou a ter 5 linhas.
2. **Correção de um bug de infraestrutura**: o arquivo `requirements.txt` (lista de dependências do projeto) estava salvo em UTF-16 em vez de UTF-8, o que podia causar falha silenciosa de instalação em alguns ambientes de deploy.
3. **Timeout na consulta WHOIS**: a consulta que verifica a idade de um domínio passou a ter um limite de tempo explícito (5 segundos), evitando que uma URL analisada trave a aplicação esperando resposta de um servidor WHOIS lento.
4. **Tratamento de erro mais preciso**: dois pontos do código que capturavam qualquer tipo de erro silenciosamente (inclusive erros que deveriam derrubar a aplicação) passaram a capturar apenas os erros esperados, com registro em log para investigação futura.
5. **Proteção contra vazamento de rede interna**: quando a aplicação resolve o endereço IP de um domínio analisado, ela agora verifica se esse IP é um endereço público de verdade. Se o domínio resolver para um endereço interno (por exemplo, um servidor local ou de infraestrutura de nuvem), o sistema trata como domínio inválido em vez de exibir esse endereço na tela.

**Por que isso importa para o relatório**: os itens 3, 4 e 5 são melhorias de segurança e confiabilidade da aplicação, algo que pode ser citado na seção de resultados como parte do amadurecimento técnico do sistema entre o PI1 e o PI2.

**Como foi validado**: o motor de cálculo do score foi testado contra os 6 cenários possíveis (URL na lista do Procon, URL barrada pelo Google, domínio inválido, domínio muito recente, domínio recente, domínio estabelecido), todos com o mesmo resultado da versão original. O fluxo completo (usuário envia URL, sistema responde) foi testado simulando as respostas das APIs externas, incluindo o caso de formulário enviado vazio (que antes quebrava a aplicação) e o caso de domínio interno/privado (que agora é bloqueado corretamente). Depois disso, o sistema também foi executado de verdade (não simulado) num navegador, analisando `google.com` de ponta a ponta com as três fontes reais (Google Safe Browsing, WHOIS, resolução de IP), confirmando que a interface segue idêntica e o resultado aparece corretamente.

**Capturas**: [`capturas/2026-08-18_fase1-home.png`](capturas/2026-08-18_fase1-home.png) (tela inicial, sem alteração visual) e [`capturas/2026-08-18_fase1-resultado-analise.png`](capturas/2026-08-18_fase1-resultado-analise.png) (resultado de uma análise real, prova de que a refatoração não quebrou nada).

**Próximo passo**: Fase 2, prevista para as Quinzenas 3–4 (07/09–04/10) — testes automatizados formais, JavaScript funcional, acessibilidade e migração do banco de dados.

---

## Fase 2 — Núcleo do edital

*Prevista para as Quinzenas 3–4 (07/09–04/10/2026); retomada e concluída em 11/10/2026 (Quinzena 5), concentrada num único dia por causa da viagem do Kemuel entre 15 e 22/10 — foge do ritmo "uma fase por quinzena", mas nenhum prazo oficial estava em risco (Relatório Final só vence 06/11, carência 15/11). Único item que depende de uma ação manual fora do código (provisionar o Postgres no Render) está marcado como pendente na última entrada abaixo.*

### Testes automatizados

**Quando**: 11/10/2026.

**Contexto**: até aqui, a validação de cada mudança era manual (rodar o fluxo no navegador, conferir visualmente). O edital pede testes automatizados, e eles também servem de rede de segurança pras próximas mudanças desta mesma fase (JavaScript sem reload, migração de banco).

**O que foi feito**: suíte com pytest em `tests/`, usando o test client do Flask e mocks das três fontes externas (Google Safe Browsing, WHOIS, resolução de IP) — o mesmo padrão já usado antes para gerar as telas do protótipo do Relatório Parcial:
- `test_scoring.py`: testes unitários do motor de regras (`calcular_resultado`), cobrindo os 6 cenários de resultado e a ordem de prioridade entre Procon, Google e idade do domínio, incluindo os limiares exatos (29/30 dias, 179/180 dias).
- `test_security_checks.py`: testes unitários de `extrair_dominio`, `resolver_ip` (IP público, privado, loopback, domínio inexistente) e `verificar_idade_dominio`/`consultar_google_safe_browsing` com as chamadas de rede mockadas.
- `test_routes.py`: testes de integração da rota `/` via test client — página inicial, formulário vazio, os 6 cenários de resultado, e se o histórico aparece depois de uma consulta.

**Como foi validado**: `pytest` executado localmente, 35 testes, todos passando (`35 passed in 4.73s`). Config em `pytest.ini`; dependência de teste isolada em `requirements-dev.txt` (não entra no deploy do Render).

### Acessibilidade e JavaScript sem reload (fetch/AJAX)

**Quando**: 11/10/2026.

**Contexto**: o formulário fazia um POST tradicional — a página inteira recarregava a cada análise. Além de menos fluido, isso também dificultava a acessibilidade: sem um reload, um leitor de tela não tem nenhum sinal automático de que o resultado mudou, a não ser que a região seja marcada explicitamente. Por isso as duas frentes foram feitas juntas.

**O que foi feito**:
1. **Acessibilidade**: campo de URL ganhou um `<label>` associado (visualmente oculto, mas lido por leitor de tela — o design só tinha um placeholder, que não substitui um label de verdade); as áreas de resultado e de histórico viraram regiões `aria-live="polite"` (sempre presentes no HTML, mesmo vazias), pra qualquer atualização de conteúdo ser anunciada automaticamente; o botão ganhou `aria-busy` refletindo o estado de carregamento, com um texto "Analisando URL, aguarde." acessível só pra leitor de tela.
2. **JavaScript sem reload**: a lógica de análise foi extraída pra uma função única (`analisar_url` em `termometro/routes.py`), reaproveitada por duas rotas: a rota `/` continua existindo exatamente como antes (POST com reload, funciona sem JavaScript); uma rota nova, `POST /api/analisar`, faz a mesma análise e devolve o resultado em JSON. `static/app.js` intercepta o envio do formulário, chama essa rota via `fetch`, e atualiza o resultado e o histórico no DOM sem recarregar a página — com checagem de `window.fetch` no início do arquivo, então em um navegador muito antigo o form volta a funcionar do jeito tradicional.

**Por que isso importa para o relatório**: cobre diretamente dois itens do núcleo do edital (script web/JavaScript e acessibilidade), e os dois ficam mais fortes um com o outro — a atualização dinâmica só é acessível porque a região tem `aria-live`.

**Como foi validado**: os 35 testes anteriores + 3 novos (`test_routes.py`) cobrindo a rota `/api/analisar` (URL em branco retorna 400, resultado correto em JSON, histórico incluído na resposta) — total 38 testes, todos passando. Além disso, verificação de ponta a ponta num navegador real (Chrome via Playwright): subimos o servidor Flask de verdade, analisamos `google.com` de verdade (mesmas três fontes reais da Fase 1), e confirmamos que (a) a página não recarrega (uma variável JavaScript marcada antes do envio sobrevive depois do resultado aparecer), (b) o estado de carregamento (`aria-busy="true"`) aparece antes do resultado, e (c) o resultado e o histórico são atualizados corretamente na tela.

**Capturas**: [`capturas/2026-10-11_fase2-fetch-sem-reload.png`](capturas/2026-10-11_fase2-fetch-sem-reload.png).

### Migração do banco de dados para PostgreSQL via SQLAlchemy

**Quando**: 11/10/2026.

**Contexto**: era o problema estrutural que mais motivou essa fase (ver "Reavaliação da stack tecnológica" acima): o SQLite vivia num arquivo local, e o plano gratuito do Render não mantém disco persistente — o histórico de consultas sumia a cada novo deploy.

**O que foi feito**: `termometro/db.py` foi reescrito usando SQLAlchemy ORM no lugar do `sqlite3` puro. Um modelo `Consulta` (mesma tabela `consultas`, mesmas colunas) substitui as queries SQL manuais. A engine é criada por uma função `init_db(database_url)`, chamada pelo `create_app()`, lendo a URL de uma variável de ambiente nova, `DATABASE_URL`:
- **Se `DATABASE_URL` não estiver definida** (dev local, ou o Render antes do Postgres ser provisionado): cai automaticamente pro mesmo arquivo SQLite de sempre. Nada muda pra quem só quer rodar o projeto localmente.
- **Se `DATABASE_URL` apontar pro Postgres**: usa Postgres de verdade, incluindo um ajuste pro formato antigo de URL (`postgres://`) que o Render ainda entrega e que o SQLAlchemy atual não aceita mais direto.
- Dependências novas em `requirements.txt`: `SQLAlchemy` e `psycopg2-binary` (binário pra não depender de compilador C no ambiente de deploy).

**Por que isso importa para o relatório**: resolve o problema estrutural citado desde a reavaliação de stack do início do PI2 — é o item que mais justifica tecnicamente essa fase.

**Como foi validado**: os 38 testes automatizados (incluindo os de histórico) passam normalmente contra o novo `db.py`, já que por padrão eles caem no SQLite temporário. Rodado também um teste de fluxo completo fora do pytest (servidor real, requisição real). Como não há Postgres disponível neste ambiente de desenvolvimento pra testar de ponta a ponta, o SQL gerado pelo SQLAlchemy foi compilado especificamente contra o dialeto do Postgres (sem conectar em nada) pra conferir que o `CREATE TABLE` é válido — saiu `SERIAL`/`VARCHAR`/`TIMESTAMP` corretos.

**Passo manual concluído**: o código por si só não trocava o banco em produção, só passava a suportar Postgres — faltava provisionar a instância gerenciada no Render e configurar `DATABASE_URL` lá, o que só quem tem acesso à conta pode fazer. Kemuel criou o banco Postgres no Render e configurou a variável de ambiente no serviço web em 11/10/2026, disparando o redeploy automático. Verificação formal em produção (confirmar que o histórico sobrevive a um novo deploy) ainda está prevista pro smoke test da Fase 4.

---

### Ajuste: correção de bug visual no histórico em telas de celular

**Quando**: 26/09/2026 (Quinzena 4).

**Contexto**: ao gerar telas do sistema como apoio visual para o Relatório Parcial, percebemos que, em telas de celular (≤480px), URLs longas no histórico de consultas quebravam no meio da palavra (por exemplo, "google.co" numa linha e "m" isolado na linha seguinte). O motivo era uma regra de CSS (`word-break: break-all`) herdada da versão para desktop, que corta o texto em qualquer ponto para caber na largura disponível, sem respeitar os limites da palavra.

**O que foi feito**: na media query que trata telas pequenas (`static/style.css`), a regra `word-break: break-all` foi trocada por `overflow-wrap: anywhere`, que só quebra a URL quando necessário e sem cortar no meio de um trecho legível, além de `max-width: 100%` e alinhamento à esquerda para o texto não estourar a largura da tela.

**Por que isso importa para o relatório**: é uma melhoria de usabilidade/acessibilidade mobile, encontrada e corrigida durante o próprio processo de revisão da interface — pode ser citada como parte do amadurecimento contínuo de UX entre o PI1 e o PI2, mesmo antes da Fase 2 formalmente começar.

**Como foi validado**: testado visualmente em larguras de 320px, 360px e 390px (celulares mais comuns), sem estouro de layout e sem quebra no meio de palavra.

**Capturas**: telas do protótipo em `capturas/prototipo-relatorio-parcial/` já refletem o CSS corrigido.

---

## Fase 3 — Diferenciais

*Prevista e concluída na Quinzena 5 (05/10–18/10/2026), em 11/10/2026 — mesmo dia da Fase 2, pelo mesmo motivo (viagem do Kemuel entre 15 e 22/10).*

### Score contínuo/ponderado e explicabilidade dos fatores

**Quando**: 11/10/2026.

**Contexto**: o motor de score (`termometro/scoring.py`) caía sempre num de 5 valores fixos (0, 10, 30, 60, 95), decididos por uma cadeia de `if/elif` sobre faixas de dias de vida do domínio. Dois domínios com 31 e 179 dias, por exemplo, recebiam exatamente o mesmo score (60) que um domínio com 1 dia a mais de diferença — e dois domínios com 1 e 29 dias também. Faltava granularidade, e o usuário não tinha como saber *por que* o score era aquele número.

**O que foi feito**:
1. **Score contínuo e ponderado**: Procon e Google Safe Browsing continuam como vetos definitivos (score 0 na hora — misturar um sinal de lista negra confirmada com sinais mais fracos deixaria o resultado perigosamente mais brando do que deveria). Fora esses dois casos, o score agora é uma combinação ponderada de dois fatores contínuos: idade do domínio via WHOIS (peso 70%, numa curva de saturação exponencial calibrada pra cruzar ~60 pontos perto dos 180 dias, o mesmo marco usado no modelo antigo) e validade da resolução de IP (peso 30% — um domínio que não resolve, ou resolve pra um endereço interno/privado, pesa contra o score). O resultado é uma nota de 0 a 100 em vez de 5 valores fixos.
2. **Explicabilidade**: `calcular_resultado` passou a devolver também uma lista `fatores`, com a descrição, o peso e a contribuição em pontos de cada sinal que formou o score. Na interface, isso aparece como um `<details>` recolhível ("Como esse score foi calculado") dentro da caixa de resultado — funciona com ou sem JavaScript, e tanto na rota com reload quanto no fetch da Fase 2 (duplicado em `static/app.js`).

**Por que isso importa para o relatório**: aborda diretamente os dois diferenciais do edital nessa frente — "score contínuo/ponderado" e "explicabilidade dos fatores do score" — e corrige uma limitação real do modelo anterior (perda de granularidade entre domínios de idades próximas).

**Como foi validado**: suíte de testes de `scoring.py` reescrita (29 testes) cobrindo: prioridade de Procon sobre Google sobre os fatores ponderados; `fonte_principal` correto nos 5 casos possíveis (procon, google, domínio inválido, IP inválido, idade normal); score sempre entre 0 e 100; monotonicidade (domínio mais antigo nunca pontua pior que um mais novo, IP inválido nunca pontua melhor que IP válido pra mesma idade); cor da faixa batendo com o score; soma das contribuições dos fatores batendo com o score final. Verificado também num navegador real: análise de `google.com` (10618 dias) retornou 100/100 com a quebra "peso 70% · contribuiu 70 pts" (idade) + "peso 30% · contribuiu 30 pts" (IP) — 70+30=100, conferindo.

**Capturas**: [`capturas/2026-10-11_fase3-explicabilidade-score.png`](capturas/2026-10-11_fase3-explicabilidade-score.png).

### Dashboard de análise de dados

**Quando**: 11/10/2026.

**Contexto**: item opcional do edital que o grupo assumiu como meta desde o início (ver "Decisão de continuar o projeto"). O histórico de consultas já existia no banco; faltava uma visão agregada dele.

**O que foi feito**: nova rota `/dashboard` (`termometro/routes.py`), com uma função de agregação `estatisticas_dashboard()` em `termometro/db.py` que lê todas as consultas registradas e calcula: distribuição de scores por faixa (seguro/atenção/perigo), os domínios mais consultados (ordenados por frequência) e a taxa de detecção por fonte — aproveitando a coluna nova `fonte_principal` (adicionada ao modelo `Consulta` nesta mesma sessão) que registra qual sinal decidiu o resultado de cada consulta (procon, google, domínio inválido, IP inválido ou idade do domínio). Renderizado em `templates/dashboard.html` com barras de progresso em CSS puro, sem nenhuma biblioteca de gráficos nova — consistente com a filosofia de frontend leve do projeto. Link pro dashboard adicionado no rodapé da página principal.

**Por que isso importa para o relatório**: cobre o item opcional de análise de dados do edital, usando dado real já coletado pela própria aplicação (sem necessidade de fonte externa).

**Como foi validado**: `tests/test_db.py` (4 testes) cobrindo a agregação isoladamente — distribuição vazia, distribuição por faixa, ordenação dos domínios mais consultados, contagem por fonte. Mais 2 testes de integração da rota `/dashboard` (estado vazio e com dados). Verificado também visualmente: populamos o banco com 10 consultas de cenários variados (incluindo Procon, Google e domínio inválido) e conferimos a olho que os números do dashboard batem exatamente com o esperado (4 seguro / 2 atenção / 4 perigo; 7 idade_dominio / 1 domínio_inválido / 1 google / 1 procon).

**Capturas**: [`capturas/2026-10-11_fase3-dashboard.png`](capturas/2026-10-11_fase3-dashboard.png).

**Nota sobre dado existente**: a coluna `fonte_principal` é nova; consultas já salvas antes dessa mudança (se existirem num banco já em produção) vão aparecer como "desconhecida" no dashboard, já que não têm esse dado retroativamente. Não é um problema agora porque a Fase 2 acabou de configurar o Postgres em produção hoje mesmo — o histórico em produção, se já existir, é recente.

---

## Fase 4 — Deploy e entrega

*Prevista para as Quinzenas 6–7 (19/10–06/11/2026). Retomada e concluída em 25/10/2026, quando Kemuel voltou da viagem. Nesse ponto, todos os itens obrigatórios do edital (framework web, banco de dados, script web/JavaScript, nuvem, uso de API, acessibilidade, controle de versão, testes) e o item opcional (análise de dados) já estavam concluídos desde a Fase 2/3 — esta fase foi sobre reprodutibilidade de deploy, integração contínua e documentação, não sobre funcionalidade pendente. Com isso, o roadmap técnico das 4 fases do PI2 está completo — falta só a redação final do relatório pelo resto do grupo.*

### Integração contínua (GitHub Actions)

**Quando**: 25/10/2026.

**Contexto**: os testes automatizados da Fase 2 só rodavam manualmente (`pytest` local). O edital pede controle de versão com qualidade contínua — ter a suíte rodando automaticamente a cada push fecha essa lacuna e evita que uma mudança quebre algo sem ninguém perceber antes de chegar em produção.

**O que foi feito**: workflow `.github/workflows/tests.yml`, rodando a cada push e pull request: instala `requirements-dev.txt` e executa `pytest` num runner Ubuntu com Python 3.12 (versão fixada só pro ambiente de CI, independente da versão usada no deploy real — ver item abaixo).

**Como foi validado**: o YAML foi validado localmente (parse sem erros) e os mesmos passos do workflow (instalar `requirements-dev.txt` + `pytest`) foram reproduzidos manualmente, 61 testes passando. A validação definitiva (rodar de verdade no GitHub) acontece no primeiro push desta fase.

### README com setup local

**Quando**: 25/10/2026.

**Contexto**: o README já documentava a arquitetura e as funcionalidades, mas não tinha nenhuma instrução de como rodar o projeto localmente — barreira pra qualquer avaliador ou novo colaborador que quisesse testar fora do deploy.

**O que foi feito**: seção nova "Rodando o projeto localmente" (clone, venv, instalação de dependências, variáveis de ambiente, como rodar a aplicação e os testes) e um arquivo `.env.example` documentando as variáveis esperadas (`GOOGLE_API_KEY` obrigatória, `DATABASE_URL` opcional). Também corrigida uma informação desatualizada no README: a seção de melhorias ainda citava `word-break: break-all` como funcionalidade ("impede mascaramento no celular"), quando na real esse foi exatamente o bug corrigido em 26/09 — o texto agora reflete a correção (`overflow-wrap: anywhere`). Tecnologias atualizadas pra citar PostgreSQL/SQLAlchemy, fetch/AJAX e pytest/GitHub Actions, que não existiam na última vez que essa seção foi escrita.

**Como foi validado**: os comandos documentados foram os mesmos efetivamente usados durante o desenvolvimento desta sessão (mesma sequência de setup).

**Versão de Python fixada**: Kemuel checou o log de build do Render e achou `Using Python version 3.14.3 (default)` — ou seja, o Render já usa 3.14.3 por conta própria, sem nada fixado no repositório (coincide com a versão usada em desenvolvimento local). Criado `.python-version` com `3.14.3` na raiz do repositório — essa é a convenção atual do Render pra fixar versão (não `runtime.txt`, que é convenção antiga do Heroku e não é lida por eles). Zero mudança de comportamento agora (mesma versão que já rodava), só torna explícito e versionado o que antes dependia do "default" do Render, que pode mudar no futuro sem aviso. `Procfile` já tinha sido feito, e o smoke test em produção já foi validado (ver entrada abaixo) — Fase 4 concluída.

### Merge pra produção e correção de um bug real de deploy (driver do Postgres)

**Quando**: 25/10/2026.

**Contexto**: ao revisar o painel do Render pra achar a versão do Python, percebemos um problema mais sério: o deploy do Render usa a branch `main`, mas Fase 2 e Fase 3 inteiras estavam só na `v2-responsividade`, nunca mescladas de volta — ou seja, nada disso estava no ar, e a variável `DATABASE_URL` configurada em produção no dia 11/10 estava sem efeito nenhum, porque o código que rodava ainda usava `sqlite3` puro e nem sabia que essa variável existia.

**O que foi feito**: aberto o PR #4 (`v2-responsividade` → `main`) no GitHub, mesclado por Kemuel. O Render disparou o redeploy automático — que falhou (`ModuleNotFoundError: No module named 'psycopg'`). A causa: o SQLAlchemy 2.1 resolve o driver padrão de uma URL `postgresql://` sem sufixo pro dialeto `psycopg` (versão 3), não mais `psycopg2` — e o `requirements.txt` só tinha `psycopg2-binary` instalado. Corrigido trocando a dependência pra `psycopg[binary]` (psycopg 3), que é o que o SQLAlchemy realmente tenta importar nessa versão.

**Por que isso importa para o relatório**: é um lembrete real de que validar a geração de SQL contra um dialeto (feito na Fase 2) não é a mesma coisa que validar a resolução do driver/dependência — a brecha só apareceu com um deploy de verdade.

**Como foi validado**: localmente, `create_engine` com uma URL Postgres fake agora resolve pro driver `psycopg` sem erro (antes, o mesmo teste reproduzia o `ModuleNotFoundError` do Render). Reinstalação limpa do `requirements.txt` num venv descartável, do zero, confirmando que a dependência certa é puxada. Os 61 testes automatizados continuam passando (não usam Postgres de verdade, então não seriam afetados por esse tipo de erro — ponto de atenção pra depois).

**Validado em produção** (25/10/2026, após o merge do PR #5): Render redeployou com sucesso. A home mostra o link novo "Ver dashboard de análise de dados" (confirma que o template atualizado está no ar) e a rota `/dashboard` carrega sem erro, mostrando "Total de consultas registradas: 0" — o zero é esperado (primeira vez que o Postgres de verdade está sendo usado, tabela recém-criada vazia), e o fato de não ter dado erro já confirma que a conexão com o banco gerenciado está funcionando. Smoke test considerado concluído pra essa frente.
