# Módulo `apis.locales`

## Sumário
- [Visão Geral](#visão-geral)
- [Estrutura do Diretório](#estrutura-do-diretório)
- [Exemplos de Arquivos YAML](#exemplos-de-arquivos-yaml)
- [Como Usar](#como-usar)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O diretório `locales/` centraliza os arquivos de tradução multilíngue da API, organizados por idioma e domínio (ex: errors, success, auth, generic). Permite fácil manutenção, expansão e integração incremental com o helper `t()` do módulo i18n.

---

## Estrutura do Diretório
```
src/visiovox/apis/locales/
├── en.yaml
├── pt.yaml
├── es.yaml
├── ru.yaml
└── cn.yaml
```
Cada arquivo representa um idioma e contém traduções organizadas por domínios.

---

## Exemplos de Arquivos YAML

### en.yaml
```yaml
errors:
  internal_server_error: "Internal server error"
  invalid_credentials: "Invalid credentials"
  not_authenticated: "Not authenticated"
  inactive_user: "User is inactive or banned"
  not_found: "Resource not found"
  rate_limited: "Too many requests. Please try again later."

success:
  operation_completed: "Operation completed successfully"
  user_authenticated: "User authenticated"
  profile_loaded: "Profile loaded successfully"

auth:
  login_success: "Welcome, {username}!"
  logout_success: "You have been logged out."
  registration_success: "Account created successfully."

generic:
  welcome: "Welcome to VisioVox Fusion, {username}!"
  goodbye: "Goodbye, see you soon!"
```

### pt.yaml
```yaml
errors:
  internal_server_error: "Erro interno do servidor"
  invalid_credentials: "Credenciais inválidas"
  not_authenticated: "Não autenticado"
  inactive_user: "Usuário inativo ou banido"
  not_found: "Recurso não encontrado"
  rate_limited: "Muitas requisições. Tente novamente mais tarde."

success:
  operation_completed: "Operação concluída com sucesso"
  user_authenticated: "Usuário autenticado"
  profile_loaded: "Perfil carregado com sucesso"

auth:
  login_success: "Bem-vindo, {username}!"
  logout_success: "Você saiu da conta."
  registration_success: "Conta criada com sucesso."

generic:
  welcome: "Bem-vindo ao VisioVox Fusion, {username}!"
  goodbye: "Até logo, volte sempre!"
```

### es.yaml
```yaml
errors:
  internal_server_error: "Error interno del servidor"
  invalid_credentials: "Credenciales inválidas"
  not_authenticated: "No autenticado"
  inactive_user: "Usuario inactivo o bloqueado"
  not_found: "Recurso no encontrado"
  rate_limited: "Demasiadas solicitudes. Por favor, inténtelo de nuevo más tarde."

success:
  operation_completed: "Operación completada con éxito"
  user_authenticated: "Usuario autenticado"
  profile_loaded: "Perfil cargado con éxito"

auth:
  login_success: "¡Bienvenido, {username}!"
  logout_success: "Has cerrado la sesión."
  registration_success: "Cuenta creada con éxito."

generic:
  welcome: "¡Bienvenido a VisioVox Fusion, {username}!"
  goodbye: "¡Hasta luego, vuelve pronto!"
```

### ru.yaml
```yaml
errors:
  internal_server_error: "Внутренняя ошибка сервера"
  invalid_credentials: "Неверные учетные данные"
  not_authenticated: "Не авторизован"
  inactive_user: "Пользователь неактивен или заблокирован"
  not_found: "Ресурс не найден"
  rate_limited: "Слишком много запросов. Пожалуйста, попробуйте позже."

success:
  operation_completed: "Операция успешно завершена"
  user_authenticated: "Пользователь аутентифицирован"
  profile_loaded: "Профиль успешно загружен"

auth:
  login_success: "Добро пожаловать, {username}!"
  logout_success: "Вы вышли из системы."
  registration_success: "Аккаунт успешно создан."

generic:
  welcome: "Добро пожаловать в VisioVox Fusion, {username}!"
  goodbye: "До свидания, до скорой встречи!"
```

### cn.yaml
```yaml
errors:
  internal_server_error: "服务器内部错误"
  invalid_credentials: "凭证无效"
  not_authenticated: "未认证"
  inactive_user: "用户未激活或被封禁"
  not_found: "未找到资源"
  rate_limited: "请求过多，请稍后再试。"

success:
  operation_completed: "操作成功完成"
  user_authenticated: "用户已认证"
  profile_loaded: "个人资料加载成功"

auth:
  login_success: "欢迎, {username}!"
  logout_success: "您已退出登录。"
  registration_success: "账号创建成功。"

generic:
  welcome: "欢迎来到VisioVox Fusion, {username}!"
  goodbye: "再见，欢迎再次使用！"
```

---

## Como Usar
Carregue e consuma as traduções via helper `t()` no código Python:

```python
from visiovox.apis.i18n import t
msg = t("errors.invalid_credentials", language="es")
# → "Credenciales inválidas"

t("auth.login_success", language="pt", username="João")
# → "Bem-vindo, João!"
```

---

## Pontos de Extensão
- Adicione novos domínios (ex: media, scene_analysis, etc) conforme necessidade dos endpoints.
- Expanda os idiomas criando novos arquivos YAML.
- Estruture mensagens para facilitar interpolação de variáveis.

---

## Notas e Recomendações
- Mantenha os arquivos YAML organizados por domínio para facilitar manutenção.
- Sempre utilize o helper `t()` para garantir fallback e interpolação.
- Traduções podem ser recarregadas em hot reload em produção, se necessário.

---

## Resumo Final
O diretório `locales/` está pronto para suportar múltiplos idiomas, domínios e integração incremental com toda a API do VisioVox Fusion. 