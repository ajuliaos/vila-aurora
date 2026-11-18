# Implementação e testes

## 1. Antes de começar
Faça snapshot das VMs. Mantenha somente as VMs necessárias ligadas. O projeto assume que o Mosquitto mTLS já funciona na vila-borda e que `~/mqtt-certs/{ca.crt,sensor.crt,sensor.key}` existe.

## 2. Copiar o projeto
Extraia o ZIP no Windows. Copie para cada VM com SCP, por exemplo:
`scp -r vila-aurora-lite aluno@192.168.56.20:~/`
Para a nuvem: `scp -r vila-aurora-lite aluno@192.168.56.10:~/`

## 3. Borda
`cd ~/vila-aurora-lite && chmod +x scripts/*.sh tests/*.sh && ./scripts/install_borda.sh`

## 4. Nuvem
`cd ~/vila-aurora-lite && chmod +x scripts/*.sh && ./scripts/install_nuvem.sh`

## 5. WireGuard
Em cada VM: instalar, gerar chave privada e pública com `wg genkey` e `wg pubkey`. Copiar somente as chaves públicas entre VMs. Basear os arquivos em `config/wireguard/*.example`, instalar como `/etc/wireguard/wg0.conf`, permissão 600 e executar `sudo systemctl enable --now wg-quick@wg0`. Validar `sudo wg show` e ping entre 10.77.0.1 e 10.77.0.2.

## 6. Executar
Na nuvem: `python3 ~/vila-aurora-lite/nuvem/api/app.py`
Na borda, terminal 1: `python3 ~/vila-aurora-lite/borda/sensores/sensor.py`
Na borda, terminal 2: `python3 ~/vila-aurora-lite/borda/buffer/sync.py`

## 7. Validar
Na borda: `cd ~/vila-aurora-lite && ./tests/teste_integracao.sh`
Resultado esperado: ping OK, health `status=ok`, contagem na nuvem e eventos locais passando gradualmente de synced=0 para synced=1.

## 8. Resiliência de 30 min
Pare somente a API da nuvem ou bloqueie temporariamente 10.77.0.1:5000. Não derrube o Mosquitto local. Deixe sensor e sync ativos por 30 minutos. Registre UTC e contagem `synced=0`. Restaure a API; aguarde sincronização; compare IDs e contagens, perda e duplicidade. Não confunda queda de NAT com indisponibilidade da nuvem.

## 9. Evidências obrigatórias
Capturas de: Mosquitto ativo; mTLS aceito; sem certificado bloqueado; WireGuard; sensor e alerta local; buffer crescendo durante falha; sincronização após retorno; contagem final; hashes SHA-256 dos logs.

## 10. Limites
Este pacote entrega o núcleo funcional otimizado: MQTT mTLS, sensor, alerta local, buffer, API idempotente, sincronização e modelos WireGuard. SIEM completo, MFA/IdP, painel WCAG, phishing controlado, IA e laudo forense exigem configuração e testes adicionais reais. Não declare esses requisitos como concluídos sem evidência.
