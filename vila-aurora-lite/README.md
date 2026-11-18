# Vila Aurora Lite - FIAP GS 2026.2

Protótipo otimizado para notebook com 8 GB de RAM.

## Topologia
- vila-nuvem: 192.168.56.10 - API e armazenamento central
- vila-borda: 192.168.56.20 - Mosquitto, sensor e buffer
- Kali: 192.168.56.30 - testes autorizados
- WireGuard: nuvem 10.77.0.1, borda 10.77.0.2

## Estado prévio esperado
Mosquitto com mTLS em 192.168.56.20:8883, CA e certificado do sensor em ~/mqtt-certs.

## Ordem
1. Leia docs/IMPLEMENTACAO_E_TESTES.md.
2. Rode scripts/install_borda.sh na vila-borda.
3. Rode scripts/install_nuvem.sh na vila-nuvem.
4. Configure WireGuard usando config/wireguard/*.example.
5. Inicie API, sensor e sincronizador.
6. Execute tests/teste_integracao.sh e o teste de resiliência de 30 min.

Nunca envie chaves privadas, senhas ou arquivos .env ao Git.
