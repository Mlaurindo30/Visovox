# Módulo `live_stream_router`

## Sumário
- [Visão Geral](#visão-geral)
- [Endpoints](#endpoints)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)
- [Histórico de Mudanças e Padronização](#histórico-de-mudanças-e-padronização)

---

## Visão Geral
O módulo `live_stream_router` expõe endpoints RESTful para controle de sessões de streaming ao vivo (iniciar, parar, status), integrando tasks Celery, autenticação opcional, schemas padronizados e respostas multilíngues.

---

## Endpoints
- `POST /live/start`: Inicia uma sessão de live stream/processamento ao vivo.
- `POST /live/stop`: Finaliza uma sessão de live stream.
- `GET /live/status/{session_id}`: Consulta status/resultados de uma sessão/processamento ao vivo.

---

## Exemplos de Uso
```python
from visiovox.apis.routers.live_stream_router import get_live_stream_router
app.include_router(get_live_stream_router())
```

---

## Pontos de Extensão
- Adição de endpoint para snapshot/capture.
- Integração com autenticação obrigatória.
- Expansão para múltiplos protocolos e tipos de entrada/saída.
- Integração futura com WebSocket API para transmissão ao vivo.

---

## Notas e Recomendações
- Sempre use schemas padronizados para entrada/saída.
- Mensagens multilíngues via helper t().
- Prefira tasks assíncronas para gravações/snapshots/processamentos demorados.

---

## Resumo Final
O módulo `live_stream_router` padroniza controle de sessões ao vivo, pronto para expansão incremental, integração com tasks, WebSocket e respostas multilíngues na API VisioVox Fusion. 

## Histórico de Mudanças e Padronização

### 2025-05-21
- **Padronização de Schemas:**
  - Todos os endpoints agora usam apenas schemas existentes e genéricos (`MediaProcessRequest`, `MediaProcessResponse`, `TaskStatusResponse`, `ErrorResponse`).
  - Reforçada a recomendação de uso de schemas genéricos para todos os domínios, exceto quando houver campos exclusivos.
- **Testes Automatizados:**
  - Testes automatizados cobrem todos os endpoints principais.
  - Mocks do Celery garantem que nenhum teste tente conexão real.
  - Cobertura de código aumentada para 76%. 