# Implementação e testes

1. Configure Mosquitto mTLS e WireGuard.
2. Exporte `VILA_API_TOKEN` com o mesmo valor em borda e nuvem.
3. Na nuvem: `python3 nuvem/api/app.py`.
4. Na borda: execute sensor e sincronizador.
5. Valide com `python3 tests/teste_integracao.py`.
6. Para resiliência, interrompa a API por 30 min, preserve o broker e comprove fila crescente; restaure, sincronize e compare UUIDs.

A API agora retorna HTTP 409 se um UUID existente chegar com conteúdo divergente. O token protege os endpoints de eventos; WireGuard continua sendo a camada de rede.
