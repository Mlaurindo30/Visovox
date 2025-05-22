# src/visiovox/core/config_manager.py

from pathlib import Path
import os
import yaml
import json
from typing import Any, Union

class ConfigManager:
    """
    Classe responsável por carregar, acessar e modificar configurações da aplicação VisioVox Fusion.
    Suporta múltiplas fontes de configuração (YAML, variáveis de ambiente) e permite overrides dinâmicos.

    A ordem de prioridade é:
    1. Overrides via `set()`
    2. Variáveis de ambiente (override_with_env)
    3. Arquivo de configuração base (YAML)
    """

    def __init__(self, config_path: Union[Path, str, None] = None) -> None:
        """
        Inicializa o ConfigManager e carrega o arquivo de configuração.

        Args:
            config_path (Path | str | None): Caminho para o arquivo YAML de configuração. 
                Se None, tenta usar 'configs/default_config.yaml'.
        """
        self._config: dict[str, Any] = {}
        self._overrides: dict[str, Any] = {}
        self._config_path = Path(config_path) if config_path else Path("configs/default_config.yaml")
        self.load_config(self._config_path)
        self.override_with_env()

    def load_config(self, path: Union[Path, str]) -> None:
        """
        Carrega o arquivo YAML de configuração.

        Args:
            path (Path | str): Caminho para o arquivo YAML.
        """
        # TODO: Implementar carregamento do YAML para self._config
        pass

    def override_with_env(self) -> None:
        """
        Substitui valores da configuração com base nas variáveis de ambiente
        que coincidam com as chaves existentes.
        """
        # TODO: Implementar lógica de override com os valores de os.environ
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retorna o valor associado a uma chave, com suporte a chaves aninhadas (ex: 'logging.level').

        Args:
            key (str): Chave no formato de dicionário aninhado (e.g. "logging.level").
            default (Any): Valor padrão caso a chave não exista.

        Returns:
            Any: Valor encontrado ou o default.
        """
        # TODO: Implementar lógica para acessar valores aninhados
        pass

    def set(self, key: str, value: Any) -> None:
        """
        Define ou sobrescreve um valor de configuração (override em runtime).

        Args:
            key (str): Chave no formato de dicionário aninhado (e.g. "models.face_swap").
            value (Any): Valor a ser atribuído.
        """
        # TODO: Implementar lógica para set aninhado
        pass

    def get_str(self, key: str, default: str = "") -> str:
        """
        Retorna o valor da configuração como string.

        Args:
            key (str): Chave de configuração.
            default (str): Valor padrão se a chave não for encontrada.

        Returns:
            str: Valor como string.
        """
        # TODO: Implementar retorno como string
        pass

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Retorna o valor da configuração como inteiro.

        Args:
            key (str): Chave de configuração.
            default (int): Valor padrão se a chave não for encontrada.

        Returns:
            int: Valor como inteiro.
        """
        # TODO: Implementar retorno como inteiro
        pass

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Retorna o valor da configuração como booleano.

        Args:
            key (str): Chave de configuração.
            default (bool): Valor padrão se a chave não for encontrada.

        Returns:
            bool: Valor como booleano.
        """
        # TODO: Implementar retorno como booleano
        pass
