# Módulo `user_models`

## Sumário
- [Visão Geral](#visão-geral)
- [Modelos Pydantic](#modelos-pydantic)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `user_models` centraliza todos os schemas Pydantic para autenticação, tokens, perfis e respostas de erro, garantindo tipagem, validação e integração com i18n.

---

## Modelos Pydantic
- `User`: Usuário base.
- `UserInDB`: Usuário com hash de senha e roles.
- `UserCreate`: Schema para registro/login.
- `Token`: Token JWT de acesso.
- `TokenPayload`: Payload do JWT.
- `UserProfile`: Perfil do usuário autenticado.
- `ErrorResponse`: Resposta de erro multilíngue.

---

## Exemplos de Uso
```python
from visiovox.apis.auth.user_models import User, UserCreate, Token
```

---

## Pontos de Extensão
- Adição de campos customizados para perfis.
- Suporte a múltiplos tipos de autenticação.
- Integração com respostas multilíngues.

---

## Notas e Recomendações
- Sempre use os schemas para validação de entrada/saída.
- Expanda conforme necessidades de domínio.

---

## Resumo Final
O módulo `user_models` padroniza schemas de autenticação, tokens e perfis, pronto para integração incremental e internacionalização na API VisioVox Fusion. 