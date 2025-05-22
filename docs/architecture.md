# Arquitetura VisioVox Fusion

## Decisões Arquiteturais Recentes (2025-05-21)

- **Padronização de Routers:**
  - Todos os routers de domínio (media, facial, voice, visual, scene, multimodal, live, model management) usam apenas schemas genéricos (`MediaProcessRequest`, `MediaProcessResponse`, `TaskStatusResponse`, `ErrorResponse`, `PaginatedResponse`).
  - Prefixos dos routers removidos dos próprios APIRouter e definidos apenas no `main.py` para evitar duplicidade de rotas.
  - Imports e handlers ajustados para não depender de schemas inexistentes ou específicos.
- **Testes Automatizados e Mocks:**
  - Testes automatizados com `pytest` cobrem todos os principais endpoints e domínios.
  - Mocks do Celery aplicados globalmente para impedir conexões reais durante os testes.
  - Ambiente Docker pronto para desenvolvimento incremental: basta subir os containers e rodar os testes sem rebuilds desnecessários.
- **Cobertura de Testes:**
  - Cobertura de código aumentada para 76%.
  - Relatório HTML de cobertura gerado em `scripts/coverage_html`.

## Diagrama de Arquitetura (TODO)

(Descreva aqui a arquitetura detalhada do sistema, diagramas, etc.) 