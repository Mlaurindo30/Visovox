from pathlib import Path
from typing import List

class ModelCacheManager:
    """
    Gerencia o cache local de modelos: espaço, LRU, TTL, limpeza.
    """

    def add_to_cache(self, model_id: str, file_path: Path) -> None:
        """
        Adiciona um modelo ao cache.

        Args:
            model_id (str): Identificador do modelo.
            file_path (Path): Caminho do arquivo do modelo.
        """
        # TODO: Implementar adição ao cache
        pass

    def remove_from_cache(self, model_id: str) -> None:
        """
        Remove um modelo do cache.

        Args:
            model_id (str): Identificador do modelo.
        """
        # TODO: Implementar remoção do cache
        pass

    def enforce_cache_policy(self) -> None:
        """
        Aplica política de cache (LRU, TTL, espaço máximo).
        """
        # TODO: Implementar política de cache
        pass

    def list_cached_models(self) -> List[str]:
        """
        Lista os modelos presentes no cache.

        Returns:
            list[str]: Identificadores dos modelos no cache.
        """
        # TODO: Listar modelos no cache
        pass

    def clear_cache(self) -> None:
        """
        Limpa todo o cache de modelos.
        """
        # TODO: Implementar limpeza total do cache
        pass 