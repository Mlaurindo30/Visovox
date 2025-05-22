# Módulo `multimodal_sync_router`

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
O módulo `multimodal_sync_router` expõe endpoints RESTful para sincronização multimodal (lip sync, gesture sync, talking head), integrando tasks Celery, autenticação opcional, schemas padronizados e respostas multilíngues.

---

## Endpoints
- `POST /sync/sync`: Submete mídia para sincronização multimodal.
- `GET /sync/status/{task_id}`: Consulta status/resultados de sincronização assíncrona.

---

## Exemplos de Uso
```python
from visiovox.apis.routers.multimodal_sync_router import get_multimodal_sync_router
app.include_router(get_multimodal_sync_router())
```

---

## Pontos de Extensão
- Adição de rotas para buscar resultados individuais, listar históricos, etc.
- Integração com autenticação obrigatória.
- Expansão para novos métodos/frameworks de sincronização.

---

## Notas e Recomendações
- Sempre use schemas padronizados para entrada/saída.
- Mensagens multilíngues via helper t().
- Prefira tasks assíncronas para operações pesadas.

---

## Resumo Final
O módulo `multimodal_sync_router` padroniza sincronização multimodal, pronto para expansão incremental, integração com tasks e respostas multilíngues na API VisioVox Fusion. 

## Histórico de Mudanças e Padronização

### 2025-05-21
- **Padronização de Schemas:**
  - Todos os endpoints agora usam apenas schemas existentes e genéricos (`MediaProcessRequest`, `MediaProcessResponse`, `TaskStatusResponse`, `ErrorResponse`).
  - Reforçada a recomendação de uso de schemas genéricos para todos os domínios, exceto quando houver campos exclusivos.
- **Testes Automatizados:**
  - Testes automatizados cobrem todos os endpoints principais.
  - Mocks do Celery garantem que nenhum teste tente conexão real.
  - Cobertura de código aumentada para 76%. 