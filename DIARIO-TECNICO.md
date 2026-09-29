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

*Escopo principal (testes automatizados, JavaScript sem reload, acessibilidade, migração para Postgres) ainda não iniciado. Prevista para as Quinzenas 3–4 (07/09–04/10/2026). Um ajuste pontual de usabilidade mobile já foi feito nessa janela, registrado abaixo.*

### Ajuste: correção de bug visual no histórico em telas de celular

**Quando**: 26/09/2026 (Quinzena 4).

**Contexto**: ao gerar telas do sistema como apoio visual para o Relatório Parcial, percebemos que, em telas de celular (≤480px), URLs longas no histórico de consultas quebravam no meio da palavra (por exemplo, "google.co" numa linha e "m" isolado na linha seguinte). O motivo era uma regra de CSS (`word-break: break-all`) herdada da versão para desktop, que corta o texto em qualquer ponto para caber na largura disponível, sem respeitar os limites da palavra.

**O que foi feito**: na media query que trata telas pequenas (`static/style.css`), a regra `word-break: break-all` foi trocada por `overflow-wrap: anywhere`, que só quebra a URL quando necessário e sem cortar no meio de um trecho legível, além de `max-width: 100%` e alinhamento à esquerda para o texto não estourar a largura da tela.

**Por que isso importa para o relatório**: é uma melhoria de usabilidade/acessibilidade mobile, encontrada e corrigida durante o próprio processo de revisão da interface — pode ser citada como parte do amadurecimento contínuo de UX entre o PI1 e o PI2, mesmo antes da Fase 2 formalmente começar.

**Como foi validado**: testado visualmente em larguras de 320px, 360px e 390px (celulares mais comuns), sem estouro de layout e sem quebra no meio de palavra.

**Capturas**: telas do protótipo em `capturas/prototipo-relatorio-parcial/` já refletem o CSS corrigido.

---

## Fase 3 — Diferenciais

*Ainda não iniciada. Prevista para a Quinzena 5 (05/10–18/10/2026).*

---

## Fase 4 — Deploy e entrega

*Ainda não iniciada. Prevista para as Quinzenas 6–7 (19/10–06/11/2026).*
