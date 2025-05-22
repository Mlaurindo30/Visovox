# Módulo `auth_router`

## Sumário
- [Visão Geral](#visão-geral)
- [Endpoints](#endpoints)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `auth_router` centraliza os endpoints RESTful de autenticação e autorização da API VisioVox Fusion, incluindo login, logout, registro, refresh e consulta de perfil. Integra dependências de autenticação, i18n e respostas multilíngues.

---

## Endpoints
- `POST /auth/login`: Autentica usuário e retorna JWT.
- `POST /auth/logout`: Invalida o token JWT atual.
- `POST /auth/register`: Registra novo usuário.
- `POST /auth/refresh`: Renova o token JWT.
- `GET /auth/me`: Retorna perfil do usuário autenticado.

Todos os endpoints utilizam schemas Pydantic e respostas multilíngues via i18n.

---

## Exemplos de Uso
```python
from visiovox.apis.auth.auth_router import get_auth_router
app.include_router(get_auth_router())
```

---

## Pontos de Extensão
- Adição de endpoints para redefinição de senha, confirmação de e-mail, etc.
- Integração com autenticação social (OAuth2 Google, etc).
- Expansão de roles/permissions por escopo.

---

## Notas e Recomendações
- Sempre utilize i18n para mensagens de erro e sucesso.
- Estruture dependências para fácil mock em testes.
- Integre com middlewares de logging e rate limit.

---

## Resumo Final
O módulo `auth_router` oferece endpoints robustos e multilíngues para autenticação JWT/OAuth2, pronto para expansão incremental e integração com toda a API VisioVox Fusion. 