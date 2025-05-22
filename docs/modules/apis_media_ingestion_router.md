# Módulo `media_ingestion_router`

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
O módulo `media_ingestion_router` expõe endpoints RESTful para ingestão, processamento e consulta de status de mídia (imagem, vídeo, áudio), integrando tasks Celery, autenticação opcional e respostas multilíngues.

---

## Endpoints
- `POST /media/process`: Submete mídia para ingestão/processamento.
- `GET /media/status/{task_id}`: Consulta status/resultados de processamento assíncrono.

---

## Exemplos de Uso
```python
from visiovox.apis.routers.media_ingestion_router import get_media_ingestion_router
app.include_router(get_media_ingestion_router())
```

---

## Pontos de Extensão
- Adição de rotas para listar mídias, buscar por ID, etc.
- Integração com autenticação obrigatória.
- Expansão para novos tipos de mídia e pipelines.

---

## Notas e Recomendações
- Sempre use schemas padronizados para entrada/saída.
- Mensagens multilíngues via helper t().
- Prefira tasks assíncronas para processamentos demorados.

---

## Resumo Final
O módulo `media_ingestion_router` padroniza ingestão e processamento de mídia, pronto para expansão incremental, integração com tasks e respostas multilíngues na API VisioVox Fusion. 

---

## Histórico de Mudanças e Padronização

### 2025-05-21
- **Padronização de Schemas:**
  - Confirmado o uso de `MediaProcessRequest` e `MediaProcessResponse` como padrão para todos os domínios de processamento de mídia.
  - Removida a necessidade de schemas específicos para cada domínio, exceto quando houver campos exclusivos.
- **Recomendações Arquiteturais:**
  - Orientação para uso de schemas genéricos sempre que possível, criando schemas específicos apenas quando necessário.
  - Sugestão de herança de schemas para futuras especializações.
- **Testes Automatizados:**
  - Testes automatizados cobrem todos os endpoints principais.
  - Mocks do Celery garantem que nenhum teste tente conexão real.
  - Cobertura de código aumentada para 76%. 