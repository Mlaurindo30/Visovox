# Módulo `apis.i18n`

## Sumário
- [Visão Geral](#visão-geral)
- [Funções Principais](#funções-principais)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `apis.i18n` centraliza a internacionalização (i18n) da API, permitindo carregar traduções multilíngues a partir de arquivos YAML, gerenciar cache em memória e fornecer uma função global `t()` para retornar mensagens traduzidas e interpoladas. Suporta fallback automático para idioma padrão e chaves aninhadas.

---

## Funções Principais

### `TranslationManager`
Classe responsável por carregar, armazenar e recuperar traduções de múltiplos idiomas, com cache em memória e fallback seguro.

#### Métodos principais:
- `load_all_translations()`: Carrega todos os arquivos YAML do diretório `locales/`.
- `get(key: str, language: str = "en", **kwargs) -> str`: Retorna a tradução para a chave e idioma, interpolando variáveis.

### `t(key: str, language: str = "en", **kwargs) -> str`
Função global para obter mensagens traduzidas, interpolando variáveis e aplicando fallback para idioma padrão ou para a chave.

---

## Exemplos de Uso

```python
from visiovox.apis.i18n import t

# Mensagem simples
msg = t("errors.invalid_credentials", language="pt")

# Mensagem com interpolação
msg2 = t("welcome", language="en", username="Maria")
```

---

## Pontos de Extensão
- Adição de novos idiomas: basta criar um arquivo YAML em `locales/` (ex: `fr.yaml`).
- Estruturação das traduções por domínio (errors, auth, success, etc).
- Hot reload das traduções em produção.
- Integração direta com middlewares, handlers e respostas da API.

---

## Notas e Recomendações
- Use sempre o helper `t()` para garantir mensagens multilíngues e interpoladas.
- Estruture os arquivos YAML de forma hierárquica para facilitar manutenção.
- O fallback seguro evita erros em produção caso traduções estejam ausentes.
- Mensagens dinâmicas são suportadas via `.format(**kwargs)`.

---

## Resumo Final
O módulo `apis.i18n` oferece uma base robusta e flexível para internacionalização da API do VisioVox Fusion, facilitando a expansão para múltiplos idiomas, domínios e mensagens dinâmicas. Sua centralização e integração incremental garantem escalabilidade e manutenção simplificada. 