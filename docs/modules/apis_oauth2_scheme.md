# Módulo `oauth2_scheme`

## Sumário
- [Visão Geral](#visão-geral)
- [Funções Principais](#funções-principais)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `oauth2_scheme` provê integração OAuth2PasswordBearer e dependência para obtenção do usuário autenticado via JWT, com suporte a i18n para erros.

---

## Funções Principais
- `oauth2_scheme`: Instância de OAuth2PasswordBearer.
- `get_current_user(token: str = Depends(oauth2_scheme), request: Request = None) -> UserInDB`: Retorna usuário autenticado ou lança erro multilíngue.

---

## Exemplos de Uso
```python
from visiovox.apis.auth.oauth2_scheme import get_current_user
```

---

## Pontos de Extensão
- Suporte a outros flows OAuth2.
- Integração com autenticação social.
- Expansão de roles e permissões.

---

## Notas e Recomendações
- Sempre use i18n para mensagens de erro.
- Estruture para fácil mock em testes.

---

## Resumo Final
O módulo `oauth2_scheme` garante autenticação segura e multilíngue, pronto para expansão incremental na API VisioVox Fusion. 