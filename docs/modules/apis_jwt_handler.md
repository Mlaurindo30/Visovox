# Módulo `jwt_handler`

## Sumário
- [Visão Geral](#visão-geral)
- [Funções Principais](#funções-principais)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `jwt_handler` centraliza helpers para geração, validação, renovação e blacklist de tokens JWT, integrando configurações seguras e suporte a roles/scopes.

---

## Funções Principais
- `create_jwt_token(user: UserInDB, scopes: List[str], expires_delta: timedelta) -> str`: Gera JWT.
- `decode_jwt_token(token: str) -> dict`: Decodifica e valida JWT.
- `refresh_jwt_token(token: str) -> str`: Renova JWT.
- `blacklist_token(token: str) -> None`: Adiciona token à blacklist.

---

## Exemplos de Uso
```python
from visiovox.apis.auth.jwt_handler import create_jwt_token, decode_jwt_token
```

---

## Pontos de Extensão
- Suporte a múltiplos algoritmos de assinatura.
- Persistência de blacklist em Redis.
- Claims customizados para roles, permissões, etc.

---

## Notas e Recomendações
- Mantenha secrets e configs em local seguro.
- Use sempre expiração curta para tokens de acesso.
- Integre com i18n para mensagens de erro.

---

## Resumo Final
O módulo `jwt_handler` oferece base robusta para autenticação JWT, pronto para expansão e integração segura na API VisioVox Fusion. 