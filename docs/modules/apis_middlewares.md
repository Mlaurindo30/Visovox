# Módulo `apis.middlewares`

## Sumário
- [Visão Geral](#visão-geral)
- [Funções Principais](#funções-principais)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `apis.middlewares` define middlewares customizados para a API FastAPI do VisioVox Fusion, focando em logging, rate limiting, internacionalização (i18n) e tratamento global de erros. Permite fácil integração plug-and-play, facilitando observabilidade, segurança e experiência multilíngue.

---

## Funções Principais

### `add_logging_middleware(app: FastAPI) -> None`
Adiciona middleware de logging para registrar requests, responses, tempo de execução e erros.

### `add_rate_limit_middleware(app: FastAPI, max_requests: int = 100, window_seconds: int = 60) -> None`
Adiciona middleware de rate limiting, limitando o número de requisições por IP em uma janela de tempo.
- **Parâmetros:**
  - `max_requests` (int): Máximo de requisições por IP.
  - `window_seconds` (int): Janela de tempo em segundos.

### `add_i18n_middleware(app: FastAPI) -> None`
Adiciona middleware de internacionalização, injetando o idioma no contexto da request a partir do header `Accept-Language`.

### `add_error_handling_middleware(app: FastAPI) -> None`
Adiciona handler global para erros/exceptions, retornando respostas padronizadas e multilíngues.

---

## Exemplos de Uso

```python
from visiovox.apis.middlewares import (
    add_logging_middleware,
    add_rate_limit_middleware,
    add_i18n_middleware,
    add_error_handling_middleware,
)

app = FastAPI()
add_logging_middleware(app)
add_rate_limit_middleware(app, max_requests=50, window_seconds=60)
add_i18n_middleware(app)
add_error_handling_middleware(app)
```

---

## Pontos de Extensão
- Logging estruturado (JSON), integração com Sentry, Prometheus, etc.
- Rate limiting robusto com Redis ou serviços externos.
- Uso de contextvars para i18n thread-safe.
- Diferenciação de exceções conhecidas/desconhecidas no handler global.
- Adição de outros middlewares (CORS custom, monitoramento, etc).

---

## Notas e Recomendações
- O rate limiting implementado é simplificado e não recomendado para produção sem backend robusto.
- Plugue os middlewares via funções para facilitar testes, mocks e evitar import cíclico.
- Expanda o handler de erros para internacionalização e logging detalhado.
- Adapte os middlewares conforme necessidades de segurança, performance e UX.

---

## Resumo Final
O módulo `apis.middlewares` oferece middlewares essenciais para robustez, segurança e internacionalização da API do VisioVox Fusion. Sua arquitetura plug-and-play facilita integração incremental e expansão futura. 