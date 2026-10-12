(function () {
    'use strict';

    if (!window.fetch) {
        // Sem fetch, o form continua funcionando do jeito tradicional (POST em '/').
        return;
    }

    var form = document.getElementById('urlForm');
    var input = document.getElementById('url');
    var btn = document.getElementById('btnAnalisar');
    var btnText = document.getElementById('btnText');
    var loader = document.getElementById('loader');
    var loaderTexto = document.getElementById('loaderTexto');
    var resultadoRegiao = document.getElementById('resultadoRegiao');
    var historicoRegiao = document.getElementById('historicoRegiao');

    function escapeHtml(valor) {
        var div = document.createElement('div');
        div.textContent = valor;
        return div.innerHTML;
    }

    function corDoScore(score) {
        if (score >= 70) return 'bg-green';
        if (score >= 40) return 'bg-orange';
        return 'bg-red';
    }

    function renderResultado(resultado, ipSite) {
        if (!resultado) {
            resultadoRegiao.innerHTML = '';
            return;
        }
        resultadoRegiao.innerHTML =
            '<div class="result-box ' + resultado.cor + '">' +
                '<h3>Resultado da Análise</h3>' +
                '<p>' + escapeHtml(resultado.status) + '</p>' +
                '<small>Score de Confiança: <strong>' + resultado.score + '/100</strong></small><br>' +
                '<small>IP do Servidor: <strong>' + escapeHtml(ipSite) + '</strong></small>' +
            '</div>';
    }

    function renderHistorico(historico) {
        if (!historico || !historico.length) {
            historicoRegiao.innerHTML = '';
            return;
        }
        var itens = historico.map(function (item) {
            return (
                '<li>' +
                    '<span class="url-hist">' + escapeHtml(item.url) + '</span>' +
                    '<span class="score-badge ' + corDoScore(item.trust_score) + '">' +
                        'Score: ' + item.trust_score +
                    '</span>' +
                '</li>'
            );
        }).join('');
        historicoRegiao.innerHTML =
            '<div class="historico-box">' +
                '<h3>Últimas Consultas</h3>' +
                '<ul>' + itens + '</ul>' +
            '</div>';
    }

    function renderErro(mensagem) {
        resultadoRegiao.innerHTML =
            '<div class="result-box res-red">' +
                '<h3>Não foi possível analisar</h3>' +
                '<p>' + escapeHtml(mensagem) + '</p>' +
            '</div>';
    }

    function estaCarregando(carregando) {
        btn.disabled = carregando;
        btn.setAttribute('aria-busy', carregando ? 'true' : 'false');
        btnText.style.display = carregando ? 'none' : '';
        loader.style.display = carregando ? 'block' : 'none';
        loaderTexto.hidden = !carregando;
    }

    form.addEventListener('submit', function (evento) {
        evento.preventDefault();

        var url = input.value.trim();
        if (!url) {
            return;
        }

        estaCarregando(true);

        var dados = new FormData();
        dados.append('url', url);

        fetch('/api/analisar', { method: 'POST', body: dados })
            .then(function (resposta) {
                if (!resposta.ok) {
                    throw new Error('Resposta inesperada do servidor (' + resposta.status + ').');
                }
                return resposta.json();
            })
            .then(function (resultadoJson) {
                renderResultado(resultadoJson.resultado, resultadoJson.ip_site);
                renderHistorico(resultadoJson.historico);
            })
            .catch(function () {
                renderErro('Falha de conexão. Confira sua internet e tente novamente.');
            })
            .finally(function () {
                estaCarregando(false);
            });
    });
})();
