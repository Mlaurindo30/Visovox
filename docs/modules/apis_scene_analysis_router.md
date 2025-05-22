# Módulo `scene_analysis_router`

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
O módulo `scene_analysis_router` expõe endpoints RESTful para análise de cena (detecção facial, landmarks, segmentação), integrando tasks Celery, autenticação opcional, schemas padronizados e respostas multilíngues.

---

## Endpoints
- `POST /scene/analyze`: Submete mídia para análise de cena.
- `GET /scene/status/{task_id}`: Consulta status/resultados de análise assíncrona.

---

## Exemplos de Uso
```python
from visiovox.apis.routers.scene_analysis_router import get_scene_analysis_router
app.include_router(get_scene_analysis_router())
```

---

## Pontos de Extensão
- Adição de rotas para buscar resultados individuais, listar análises, etc.
- Integração com autenticação obrigatória.
- Expansão para novos algoritmos/modelos de análise.

---

## Notas e Recomendações
- Sempre use schemas padronizados para entrada/saída.
- Mensagens multilíngues via helper t().
- Prefira tasks assíncronas para análises demoradas.

---

## Resumo Final
O módulo `scene_analysis_router` padroniza análise de cena, pronto para expansão incremental, integração com tasks e respostas multilíngues na API VisioVox Fusion. 

---

## Histórico de Mudanças e Padronização

### 2025-05-21
- **Padronização de Schemas:**
  - Todos os endpoints agora usam apenas schemas existentes e genéricos (`MediaProcessRequest`, `MediaProcessResponse`, `TaskStatusResponse`, `ErrorResponse`).
  - Reforçada a recomendação de uso de schemas genéricos para todos os domínios, exceto quando houver campos exclusivos.
- **Recomendações Arquiteturais:**
  - Orientação para uso de schemas genéricos sempre que possível, criando schemas específicos apenas quando necessário.
  - Sugestão de herança de schemas para futuras especializações.
- **Testes Automatizados:**
  - Testes automatizados cobrem todos os endpoints principais.
  - Mocks do Celery garantem que nenhum teste tente conexão real.
  - Cobertura de código aumentada para 76%. 