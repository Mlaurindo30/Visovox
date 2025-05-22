# Testes Automatizados — VisioVox Fusion

## Estratégia de Testes

- Todos os endpoints principais da API são testados via `pytest` e `TestClient` do FastAPI.
- O ambiente de testes é executado dentro do container Docker da API, garantindo isolamento e reprodutibilidade.
- Mocks do Celery são aplicados globalmente para impedir qualquer tentativa de conexão real com o broker (Redis/RabbitMQ).
- A cobertura de código é medida com `pytest-cov` e relatórios HTML são gerados em `scripts/coverage_html`.

---

## Mocks do Celery

- Para evitar dependência de infraestrutura externa, todos os métodos `.delay` e `.apply_async` das tasks Celery são mockados nos testes.
- O mock é aplicado tanto no caminho do módulo de tasks (`src.visiovox.apis.celery_tasks`) quanto no caminho do handler do router, garantindo interceptação total.
- Para máxima robustez, o método global `celery.app.task.Task.apply_async` também é mockado, impedindo qualquer execução real de task.

### Exemplo de Mock
```python
import celery.app.task
monkeypatch.setattr(celery.app.task.Task, "apply_async", lambda self, *args, **kwargs: type("T", (), {"id": "12345"})())
```

---

## Estrutura dos Testes

- Todos os testes estão em `tests/apis/test_router.py`.
- Cada teste cobre um endpoint principal (media, facial, voice, visual, scene, multimodal, live, models).
- O client do FastAPI é criado via fixture pytest, garantindo que o mock do Celery seja aplicado antes do carregamento do app.

### Exemplo de Teste
```python
def test_process_media_ok(monkeypatch):
    import celery.app.task
    monkeypatch.setattr(celery.app.task.Task, "apply_async", lambda self, *args, **kwargs: type("T", (), {"id": "12345"})())
    from src.visiovox.apis.main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    with open("tests/assets/sample.jpg", "rb") as f:
        response = client.post(
            "/api/v1/media/process",
            data={"media_type": "image"},
            files={"file": ("sample.jpg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    assert "task_id" in response.json()
```

---

## Cobertura de Testes

- A cobertura de código dos endpoints principais está em 76%.
- Para aumentar a cobertura, basta adicionar novos testes para casos de erro, autenticação, parâmetros inválidos, etc.
- O relatório HTML pode ser visualizado em `scripts/coverage_html/index.html` após rodar:
  ```bash
  docker compose exec api poetry run pytest --cov=src --cov-report=html:./scripts/coverage_html
  ```

---

## Troubleshooting

- **Erro de conexão com Celery:**
  - Certifique-se de que o mock global de `celery.app.task.Task.apply_async` está ativo antes de importar o app.
  - Se necessário, mova o import do app e do client para dentro do teste.
- **404 em endpoints:**
  - Verifique se o router está incluído corretamente no `main.py` e se o prefixo não está duplicado.
- **Schemas inexistentes:**
  - Todos os endpoints devem usar apenas schemas genéricos (`MediaProcessRequest`, `MediaProcessResponse`, etc.).
- **Testes não reconhecem o mock:**
  - Use sempre o `monkeypatch` do pytest e garanta que o mock é aplicado antes do carregamento do app.

---

## Resumo das Mudanças Realizadas

- **Padronização dos Routers:**
  - Todos os routers usam apenas schemas genéricos, removendo dependências de schemas inexistentes.
  - Prefixos dos routers definidos apenas no `main.py`.
- **Mocks do Celery:**
  - Mock global de `apply_async` garante que nenhum teste tente conexão real.
- **Testes Automatizados:**
  - Todos os endpoints principais cobertos.
  - Fixture pytest para client e mocks.
- **Fluxo Docker:**
  - Testes executados dentro do container, sem rebuilds desnecessários.
- **Cobertura:**
  - 76% de cobertura, com relatório HTML disponível.

---

## Como Rodar os Testes

1. Suba os containers:
   ```bash
   docker compose up -d
   ```
2. Execute os testes dentro do container da API:
   ```bash
   docker compose exec api poetry run pytest --cov=src
   ```
3. O relatório de cobertura será gerado em `scripts/coverage_html`.

---

## Próximos Passos

- Adicionar testes para autenticação, erros e casos de borda.
- Expandir mocks para tasks futuras.
- Manter a documentação sempre atualizada a cada mudança de arquitetura ou fluxo de testes. 