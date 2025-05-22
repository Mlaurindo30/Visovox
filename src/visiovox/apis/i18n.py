# src/visiovox/apis/i18n.py

import os
import yaml
from typing import Dict, Any

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")
DEFAULT_LANGUAGE = "en"

class TranslationManager:
    """
    Gerencia o carregamento, cache e recuperação de traduções multilíngues.
    """

    def __init__(self, locales_dir: str = LOCALES_DIR) -> None:
        self.locales_dir = locales_dir
        self._translations: Dict[str, Dict[str, Any]] = {}
        self.load_all_translations()

    def load_all_translations(self) -> None:
        """
        Carrega todos os arquivos de tradução YAML do diretório locales/.
        """
        for filename in os.listdir(self.locales_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                lang = filename.split(".")[0]
                file_path = os.path.join(self.locales_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        self._translations[lang] = yaml.safe_load(f) or {}
                    except Exception as e:
                        print(f"[i18n] Erro ao carregar {filename}: {e}")

    def get(self, key: str, language: str = DEFAULT_LANGUAGE, **kwargs) -> str:
        """
        Retorna a tradução correspondente à chave para o idioma especificado.
        Suporta chaves aninhadas (ex: "errors.invalid_credentials").
        Faz fallback para idioma padrão se não encontrar.

        Args:
            key (str): Chave da mensagem (ex: "errors.invalid_credentials").
            language (str): Código do idioma ("en", "pt", ...).
            kwargs: Variáveis para interpolação (ex: username="João").

        Returns:
            str: Mensagem traduzida.
        """
        msg = self._resolve_key(key, language)
        # Fallback para idioma padrão se não encontrado
        if msg is None and language != DEFAULT_LANGUAGE:
            msg = self._resolve_key(key, DEFAULT_LANGUAGE)
        if msg is None:
            return key  # Retorna chave como último fallback
        try:
            return msg.format(**kwargs)
        except Exception:
            return msg

    def _resolve_key(self, key: str, language: str) -> Any:
        """
        Busca valor para chave aninhada em dicionário de traduções.
        """
        translation = self._translations.get(language, {})
        for part in key.split("."):
            if isinstance(translation, dict) and part in translation:
                translation = translation[part]
            else:
                return None
        return translation

# Instância global (singleton) do gerenciador de traduções
_translation_manager = TranslationManager()

def t(key: str, language: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Helper global para retornar traduções.

    Args:
        key (str): Chave da mensagem.
        language (str, opcional): Idioma (default "en").
        kwargs: Variáveis para interpolação.

    Returns:
        str: Mensagem traduzida, interpolada.
    """
    return _translation_manager.get(key, language, **kwargs)

# Exemplo de uso:
# t("errors.invalid_credentials", language="pt")
# t("welcome", language="en", username="Maria")

# Notas e Recomendações
# Para adicionar um novo idioma, basta criar um arquivo YAML em locales/ com o código do idioma (ex: fr.yaml).
# Estruture as traduções por domínio (errors, auth, success, etc) para facilitar organização e manutenção.
# O método .format(**kwargs) permite mensagens dinâmicas (ex: "Bem-vindo, {username}!").
# Em produção, considere recarregar as traduções automaticamente se os arquivos mudarem (hot reload, opcional).
# Pronto para integração incremental: use o helper t() em todos os endpoints, handlers e middlewares para mensagens multilíngues. 