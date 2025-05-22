# Módulo `apis.dependencies`

## Sumário
- [Visão Geral](#visão-geral)
- [Funções Principais](#funções-principais)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `apis.dependencies` centraliza dependências FastAPI para autenticação, autorização, contexto multilíngue (i18n) e acesso a recursos globais (settings, orchestrator, celery, etc.). Facilita a injeção de contexto, segurança e modularização dos endpoints, além de permitir fácil mock em testes.

---

## Funções Principais

### `get_settings() -> Any`
Retorna as configurações globais da API. Ideal para acesso seguro e tipado a settings/configs.

### `get_i18n_language(request: Request) -> str`
Obtém o idioma corrente da request, podendo analisar header, param, cookie ou perfil autenticado.

### `get_current_user(request: Request) -> Any`
Recupera o usuário autenticado a partir do JWT/OAuth2 no header Authorization. Lança exceção 401 se não autenticado.

### `get_active_user(current_user: Any = Depends(get_current_user)) -> Any`
Verifica se o usuário autenticado está ativo. Lança exceção 403 se inativo/banido.

---

## Exemplos de Uso

```python
from visiovox.apis.dependencies import get_current_user, get_i18n_language
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/me")
async def get_profile(user = Depends(get_current_user), lang = Depends(get_i18n_language)):
    return {"user": user, "lang": lang}
```

---

## Pontos de Extensão
- Suporte a múltiplas estratégias de autenticação (JWT, OAuth2, API Key).
- Integração de preferências de idioma do usuário autenticado.
- Dependências para orchestrator, celery, db, etc., facilitando desacoplamento e integração de pipelines/tasks.
- Modularização por domínio (permissões avançadas, recursos de background, etc.).

---

## Notas e Recomendações
- Prefira dependências explicitamente tipadas para facilitar testes e documentação automática.
- Expanda as dependências conforme surgirem novos domínios e recursos globais.
- Use mocks/fakes em testes para desacoplar lógica de autenticação/autorização.

---

## Resumo Final
O módulo `apis.dependencies` padroniza a injeção de contexto, autenticação, autorização e recursos globais nos endpoints da API do VisioVox Fusion. Pronto para expansão incremental e integração robusta com os demais domínios da plataforma. 