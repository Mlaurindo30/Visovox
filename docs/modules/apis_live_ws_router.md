# Módulo `live_ws_router`

## Sumário
- [Visão Geral](#visão-geral)
- [Endpoints WebSocket](#endpoints-websocket)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `live_ws_router` expõe endpoints WebSocket para transmissão ao vivo de feedback, notificações, progresso de tarefas e broadcast de eventos. Pronto para autenticação JWT/OAuth2, respostas multilíngues (i18n) e integração com filas/broadcast.

---

## Endpoints WebSocket
- `GET /ws/live`: Conexão WebSocket para feedback ao vivo, broadcast e integração com tasks.

---

## Exemplos de Uso
```python
from visiovox.apis.websocket.live_ws_router import get_live_ws_router
app.include_router(get_live_ws_router())
```

---

## Pontos de Extensão
- Integração com autenticação JWT/OAuth2 (Depends).
- Broadcast multiusuário com Redis PubSub, Celery, etc.
- Criação de arquivos auxiliares: `broadcast_manager.py`, `ws_events.py`.
- Suporte a múltiplos tópicos/eventos (ex: /ws/notifications).

---

## Notas e Recomendações
- Sempre use o helper `t()` para mensagens multilíngues.
- Prepare para integração incremental com tasks, orquestrador e frontend.
- Estruture para fácil expansão e testes.

---

## Resumo Final
O módulo `live_ws_router` oferece base robusta e expansível para conexões WebSocket autenticadas, broadcast e feedback ao vivo na API VisioVox Fusion. 