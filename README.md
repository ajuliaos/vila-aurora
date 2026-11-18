# Vila Aurora - Global Solution FIAP 2026.2

Protótipo acadêmico de infraestrutura comunitária resiliente, otimizado para notebook com 8 GB de RAM.

## Componentes
- **vila-aurora-lite:** sensor MQTT/mTLS, alerta local, buffer SQLite, sincronização idempotente, API Flask e modelos WireGuard.
- **vila-aurora-complemento:** painel, monitoramento, resposta a incidentes, phishing defensivo, IA com avaliação holdout, laboratório de SQL Injection, forense e documentação de viabilidade.

## Resultados já demonstrados no laboratório
- MQTT mTLS com certificado válido aceito e cliente sem certificado recusado.
- WireGuard entre `10.77.0.1` e `10.77.0.2`.
- Store-and-forward com 457 UUIDs correspondentes entre borda e nuvem.
- Painel web, regras sintéticas de detecção, SQLi segura/vulnerável isolada e hashes SHA-256.

## Segurança
O repositório não contém chaves privadas, senhas, bancos operacionais nem arquivos `.env`. Copie `.env.example` para `.env` apenas no ambiente local e nunca versione o arquivo real.
