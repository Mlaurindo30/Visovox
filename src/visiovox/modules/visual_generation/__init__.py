"""
Módulo visual_generation
-----------------------
Hub de interfaces e implementações para geração visual condicional/criativa (GAN, Diffusion, etc) no VisioVox Fusion.

- Extensível: plugue novos modelos facilmente (ex: DALL·E, SDXL, DreamBooth).
- Integração: pronto para uso em pipelines e orquestrador.
- Testabilidade: fácil de mockar/fakear para testes unitários.

Padrão de uso:
    from visiovox.modules.visual_generation import StyleGANEXVisualGenerator, StableDiffusionGenerator

Notas:
- Sempre documente o formato de input/output nas docstrings das implementações concretas.
- Prefira tipos explícitos: np.ndarray, PIL.Image, str/path.
- Veja exemplos e recomendações nos arquivos styleganex_processor.py e diffusion_processor.py.
"""

from .styleganex_processor import BaseVisualGenerator, StyleGANEXVisualGenerator

# Opcional: Diffusion pode depender de libs pesadas, então o import é protegido
try:
    from .diffusion_processor import BaseDiffusionGenerator, StableDiffusionGenerator
except ImportError:
    BaseDiffusionGenerator = None
    StableDiffusionGenerator = None

__all__ = [
    "BaseVisualGenerator",
    "StyleGANEXVisualGenerator",
    "BaseDiffusionGenerator",
    "StableDiffusionGenerator"
]

# --- Notas para desenvolvedores ---
# - Para expandir: crie novas classes seguindo o padrão ABC e registre aqui.
# - Integração: pronto para ser consumido pelo Orchestrator/pipeline manager.
# - Testes: utilize mocks/fakes das interfaces base para testes unitários. 