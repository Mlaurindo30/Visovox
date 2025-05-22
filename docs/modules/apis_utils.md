# Módulo `apis.utils`

## Sumário
- [Visão Geral](#visão-geral)
- [Funções Principais](#funções-principais)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `apis.utils` centraliza utilitários para padronização de respostas da API, parsing de parâmetros e helpers para internacionalização e manipulação de dados em endpoints FastAPI. Facilita a consistência, extensibilidade e internacionalização das respostas, além de simplificar o tratamento de tipos comuns em queries e bodies.

---

## Funções Principais

### `success_response`
Gera uma resposta padronizada de sucesso para endpoints da API.
- **Parâmetros:**
  - `data` (Any): Dados de retorno.
  - `message` (str, opcional): Mensagem de sucesso.
  - `language` (str, opcional): Idioma da resposta.
  - `status_code` (int, opcional): Código HTTP.
- **Retorno:** `dict` padronizado com status, mensagem, dados, código e request_id.

### `error_response`
Gera uma resposta padronizada de erro para endpoints da API.
- **Parâmetros:**
  - `error_code` (str): Código do erro (internacionalizável).
  - `message` (str, opcional): Mensagem do erro.
  - `language` (str, opcional): Idioma da resposta.
  - `status_code` (int, opcional): Código HTTP.
  - `details` (Any, opcional): Dados adicionais sobre o erro.
- **Retorno:** `dict` padronizado com status, código do erro, mensagem, detalhes, código e request_id.

### `get_language_from_request`
Extrai o idioma preferencial da requisição a partir do header `Accept-Language`.
- **Parâmetros:**
  - `request` (Request): Objeto da requisição FastAPI.
- **Retorno:** Código do idioma (`str`).

### `parse_bool`
Converte valores diversos em booleano, útil para parsing de query/body.
- **Parâmetros:**
  - `value` (Any): Valor a ser convertido.
- **Retorno:** Booleano (`bool`).

### `parse_list`
Converte valor em lista, útil para query/body params múltiplos.
- **Parâmetros:**
  - `value` (Any): Valor a ser convertido.
- **Retorno:** Lista (`list`).

---

## Exemplos de Uso

```python
from visiovox.apis.utils import success_response, error_response, parse_bool, parse_list

# Exemplo de resposta de sucesso
resp = success_response(data={"foo": "bar"}, message="Operação realizada com sucesso", language="pt")

# Exemplo de resposta de erro
err = error_response(error_code="INVALID_INPUT", message="Parâmetro inválido", language="pt", details={"param": "id"})

# Parsing de booleano
flag = parse_bool("sim")  # True

# Parsing de lista
lst = parse_list("a,b,c")  # ["a", "b", "c"]
```

---

## Pontos de Extensão
- Internacionalização: integração futura com helper `t()` para tradução automática de mensagens.
- Adição de novos helpers para logs, validação de paths, UUIDs seguros, etc.
- Customização dos formatos de resposta conforme necessidades do frontend ou clientes externos.

---

## Notas e Recomendações
- Sempre utilize os helpers de resposta para garantir consistência e rastreabilidade (request_id).
- Para projetos multilíngues, priorize a integração com o módulo de i18n.
- Expanda os parsers conforme surgirem novos tipos de parâmetros recorrentes.

---

## Resumo Final
O módulo `apis.utils` é essencial para padronização, internacionalização e robustez das respostas da API do VisioVox Fusion. Sua expansão incremental é recomendada conforme o crescimento das necessidades do projeto. 