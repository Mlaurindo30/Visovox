# Módulo `model_management_router`

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
O módulo `model_management_router` expõe endpoints RESTful para gerenciamento de modelos (listar, baixar, status, remover), integrando tasks Celery, autenticação opcional, schemas padronizados e respostas multilíngues.

---

## Endpoints
- `GET /models/list`: Lista todos os modelos disponíveis/baixados.
- `POST /models/download`: Solicita download de um modelo específico.
- `GET /models/status/{model_id}`: Consulta status/resultados de download/verificação.
- `DELETE /models/remove/{model_id}`: Remove modelo do cache local.

---

## Exemplos de Uso
```python
from visiovox.apis.routers.model_management_router import get_model_management_router
app.include_router(get_model_management_router())
```

---

## Pontos de Extensão
- Adição de endpoint para atualização/verificação de modelos.
- Integração com autenticação obrigatória.
- Expansão para múltiplos provedores, tipos de modelo, campos customizados.

---

## Notas e Recomendações
- Sempre use schemas padronizados para entrada/saída.
- Mensagens multilíngues via helper t().
- Prefira tasks assíncronas para downloads/updates pesados.

---

## Resumo Final
O módulo `model_management_router` padroniza gerenciamento de modelos, pronto para expansão incremental, integração com tasks, múltiplos provedores e respostas multilíngues na API VisioVox Fusion. 

---

## Histórico de Mudanças e Padronização

### 2025-05-21
- **Padronização de Schemas:**
  - Todos os endpoints agora usam apenas schemas existentes e genéricos (`MediaProcessRequest`, `MediaProcessResponse`, `TaskStatusResponse`, `ErrorResponse`).
  - Reforçada a recomendação de uso de schemas genéricos para todos os domínios, exceto quando houver campos exclusivos.
- **Testes Automatizados:**
  - Testes automatizados cobrem todos os endpoints principais.
  - Mocks do Celery garantem que nenhum teste tente conexão real.
  - Cobertura de código aumentada para 76%. 