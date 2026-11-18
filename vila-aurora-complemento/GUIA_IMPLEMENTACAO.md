# Guia de implementação e validação

## Entregue pronto
Painel Flask leve; perfis operador/auditor; quatro regras; laboratório SQLi isolado; simulação defensiva de phishing; modelo Isolation Forest; utilitários forenses; modelos de relatórios; instalador e smoke test.

## Você ainda precisa executar
1. Copiar esta pasta para a vila-nuvem.
2. Rodar `./scripts/install_complemento.sh`.
3. Definir senhas e segredo em variáveis de ambiente, sem registrar no Git.
4. Subir primeiro ZIP e WireGuard; confirmar eventos em `~/vila-aurora-lite/data/nuvem.db`.
5. Iniciar painel: `export VILA_SECRET_KEY='valor-aleatorio-forte'`; definir `VILA_OPERADOR_PASSWORD` e `VILA_AUDITOR_PASSWORD`; executar `python3 dashboard/app.py`.
6. Acessar apenas pelo túnel: `http://10.77.0.1:8080`.
7. Rodar `./tests/run_smoke.sh` e guardar evidências.
8. Executar testes reais de mTLS, VPN, segmentação, SQLi seguro e vulnerável isolado, quatro alertas, IA e caos de 30 min.
9. Preencher E1, E3 e E4 com resultados reais, capturas, UTC e hashes.

## Painel
As senhas padrão no código são somente fallback de demonstração e DEVEM ser substituídas por variáveis de ambiente. O protótipo não comprova MFA. Para RT-09, integrar IdP com MFA ou documentar como lacuna.

## Monitoramento
`python3 monitoramento/regras.py < monitoramento/eventos_teste.jsonl` deve gerar quatro alertas. Depois substitua eventos sintéticos por logs reais normalizados e centralizados. O motor leve não é, sozinho, um SIEM completo.

## SQLi
Por padrão apenas `/seguro` existe. Para demonstrar a falha isolada: `LAB_VULNERAVEL=1 python3 seguranca/sqli_lab.py`, somente em localhost e com dados sintéticos. Compare com `/seguro`; pare logo após a evidência.

## IA
`python3 ia/treinar_anomalias.py` gera CSV, modelo e métricas sintéticas. Identifique explicitamente os dados como sintéticos. Registre matriz de confusão, precisão, recall e taxa de falsos positivos.

## Forense
Copie logs/capturas para `evidencias/`, execute `python3 forense/coletar_hashes.py evidencias` e preencha cadeia de custódia e timeline. Não altere evidências após o hash.

## O que permanece pendente de implementação/validação real
MFA/IdP; SIEM completo; CRL/revogação efetiva; domínio DNS com SPF/DKIM/DMARC; campanha controlada; painel validado WCAG; custos; RIPD LGPD; manutenção; teste de caos; laudo final; vídeo, se exigido pelo canal da disciplina.
