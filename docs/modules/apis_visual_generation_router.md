# Módulo `visual_generation_router`

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
O módulo `visual_generation_router` expõe endpoints RESTful para geração visual (imagens sintéticas, manipulação criativa), integrando tasks Celery, autenticação opcional, schemas padronizados e respostas multilíngues.

---

## Endpoints
- `POST /visual/generate`: Gera imagem(s) sintética(s) a partir de prompt/parâmetros.
- `GET /visual/status/{task_id}`: Consulta status/resultados de geração visual assíncrona.

---

## Exemplos de Uso
```python
from visiovox.apis.routers.visual_generation_router import get_visual_generation_router
app.include_router(get_visual_generation_router())
```

---

## Pontos de Extensão
- Adição de rotas para buscar resultados individuais, listar históricos, etc.
- Integração com autenticação obrigatória.
- Expansão para novos modelos/backends de geração visual.

---

## Notas e Recomendações
- Sempre use schemas padronizados para entrada/saída.
- Mensagens multilíngues via helper t().
- Prefira tasks assíncronas para operações pesadas.

---

## Resumo Final
O módulo `visual_generation_router` padroniza geração visual, pronto para expansão incremental, integração com tasks e respostas multilíngues na API VisioVox Fusion. 

---

## Histórico de Mudanças e Padronização

### 2025-05-21
- **Padronização de Schemas:**
  - Removido o uso de `VisualGenerationRequest` e `VisualGenerationResponse`, padronizando para `MediaProcessRequest` e `MediaProcessResponse` para evitar duplicidade e garantir compatibilidade com o restante da API.
  - Ajustados imports e tipos de resposta dos endpoints para refletir os schemas existentes em `schemas.py`.
- **Diagnóstico Minucioso:**
  - Análise detalhada dos erros de importação e ausência de schemas, com recomendações arquiteturais para padronização e expansão futura.
- **Recomendações Arquiteturais:**
  - Orientação para uso de schemas genéricos sempre que possível, criando schemas específicos apenas quando necessário.
  - Sugestão de herança de schemas para futuras especializações.
- **Testes Automatizados:**
  - Testes automatizados cobrem todos os endpoints principais.
  - Mocks do Celery garantem que nenhum teste tente conexão real.
  - Cobertura de código aumentada para 76%. 