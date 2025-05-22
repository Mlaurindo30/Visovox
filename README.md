# VisioVox Fusion

Plataforma IA multimodal para manipulação facial e vocal, com arquitetura modular, extensível e pronta para produção. Suporta operação offline (CLI/GUI) e API distribuída (FastAPI + Celery + Redis).

---

## Estrutura do Projeto

```
visiovox-fusion-platform/
├── configs/
├── docs/
├── logs/
├── models/
├── notebooks/
├── scripts/
├── src/
│   └── visiovox/
│       ├── apis/
│       ├── cli/
│       ├── core/
│       │   ├── config_manager.py
│       │   ├── logger_setup.py
│       │   ├── resource_manager.py
│       │   ├── orchestrator.py
│       │   ├── pipeline_manager.py
│       │   └── __init__.py
│       ├── gui/
│       ├── integrations/
│       ├── modules/
│       ├── tasks/
│       └── utils/
├── tests/
├── Dockerfile_api
├── Dockerfile_worker
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## Núcleo (Core) — Primeiros Componentes

> **Nota:** O arquivo `__init__.py` do módulo `core` expõe explicitamente os principais componentes (`ConfigManager`, `setup_logging`, `ResourceManager`, `Orchestrator`, `PipelineManager`) para facilitar a importação em outros módulos do projeto:
>
> ```python
> from visiovox.core import ConfigManager, setup_logging, ResourceManager, Orchestrator, PipelineManager
> ```

### 1. `config_manager.py`

#### Análise Pré-Código
**Responsabilidades:**
- Carregar configurações da aplicação a partir de múltiplas fontes: arquivos YAML, variáveis de ambiente e (eventualmente) arquivos JSON.
- Suportar overrides de configuração com prioridade (ex: variáveis de ambiente sobrescrevem YAML).
- Fornecer acesso tipado e seguro a valores de configuração (como get_int, get_bool, etc.).
- Suportar perfis diferentes (ex: produção, desenvolvimento, usuário).

**Classe Principal:** ConfigManager

**Métodos Principais:**
- `__init__(config_path: Path | str | None = None)`
  - Inicializa a instância e carrega o arquivo de configuração default e qualquer sobreposição via env.
- `load_config(path: Path | str) -> None`
  - Carrega o YAML da configuração principal (e.g., configs/default_config.yaml).
- `override_with_env() -> None`
  - Sobrescreve valores da configuração com variáveis de ambiente se existirem.
- `get(key: str, default: Any = None) -> Any`
  - Acesso genérico a um valor de configuração por chave aninhada (ex: logging.level).
- `set(key: str, value: Any) -> None`
  - Define ou sobrescreve um valor de configuração via chave aninhada.
- `get_str(key: str, default: str = "") -> str`
  - Retorna o valor da chave como string.
- `get_int(key: str, default: int = 0) -> int`
  - Retorna o valor como inteiro.
- `get_bool(key: str, default: bool = False) -> bool`
  - Retorna o valor como booleano.

**Status:** Esqueleto criado com docstrings e pontos de extensão (TODOs) para implementação futura.

### 2. `logger_setup.py`

#### Análise Pré-Código
**Responsabilidades:**
- Configurar um sistema de logging unificado para toda a aplicação (console, arquivo, JSON se necessário).
- Definir níveis e formatos de log, baseados nas configurações fornecidas (ConfigManager ou dicionário).
- Permitir reconfiguração dinâmica, se necessário.
- Fornecer integração simples (ex: basta importar e chamar setup_logging).

**Função Principal:**
- `setup_logging(config: ConfigManager | dict) -> None`
  - Propósito: Configurar o sistema de logging global conforme as configurações.
  - Parâmetros: config (ConfigManager | dict): Configuração para logging (nível, formatos, handlers).
  - Retorno: None

**(Opcional)**
- Classe LoggerSetup: Caso precise de um setup mais elaborado (para logs dinâmicos, reconfiguração ou handlers customizados), pode envolver uma classe.

**Status:** Esqueleto criado, pronto para receber implementação dinâmica baseada em configuração.

### 3. `resource_manager.py`

#### Análise Pré-Código
**Responsabilidades:**
- Gerenciar o ciclo de vida de modelos de IA (carregamento, descarregamento, cache, awareness de VRAM).
- Prover métodos para obter modelos de acordo com o tipo e nome.
- Gerenciar pool de recursos computacionais (CPU/GPU).
- Permitir verificações sobre disponibilidade de memória/VRAM.
- Lidar com descarte (liberação) de modelos não utilizados (LRU).

**Classe Principal:** ResourceManager

**Métodos Principais:**
- `__init__(config: ConfigManager | dict)`
  - Inicializa gerenciador de recursos com configurações.
  - Parâmetros: configuração global (ConfigManager ou dict).
- `get_model(model_name: str, model_type: str) -> Any`
  - Retorna uma instância carregada do modelo solicitado (do cache ou carregando do disco).
  - Parâmetros: nome e tipo do modelo.
  - Retorno: objeto do modelo (tipagem Any por ser genérico).
- `release_model(model_name: str) -> None`
  - Libera recursos do modelo indicado, removendo do cache se necessário.
- `check_vram_availability(required_vram: int) -> bool`
  - Verifica se há VRAM suficiente para carregar um novo modelo.
  - Parâmetros: quantidade de VRAM requerida (em MB).
  - Retorno: bool.
- `list_loaded_models() -> list[str]`
  - Lista nomes dos modelos atualmente carregados em memória.
- (Opcional, mas recomendado): métodos para obter recursos computacionais, stats de GPU, uso de memória etc.

**Status:** Esqueleto criado, com docstrings detalhadas e TODOs para implementação futura.

### 4. `orchestrator.py`

#### Análise Pré-Código
**Responsabilidades:**
- Coordenar a execução de pipelines completos (ex: face swap em vídeo).
- Interagir com PipelineManager, ResourceManager e outros módulos funcionais.
- Permitir rodar pipelines pré-definidos (ex: pipeline de face swap, pipeline de sincronização face+voz).
- Aceitar dados de entrada, configurações sobrescritas e retornar resultados.

**Classe Principal:** Orchestrator

**Métodos Principais:**
- `__init__(config: ConfigManager | dict, resource_manager: ResourceManager, pipeline_manager: PipelineManager | None = None)`
  - Inicializa com as dependências principais (gerenciamento de config, recursos e pipelines).
- `run_pipeline(pipeline_name: str, input_data: Any, config_overrides: dict | None = None) -> Any`
  - Executa um pipeline identificado pelo nome.
  - Parâmetros: nome do pipeline, dados de entrada, overrides de configuração (opcional).
  - Retorno: saída/resultados do pipeline.
- `run_video_face_voice_sync_pipeline(video_path: str, face_image_path: str, target_voice_model: str, output_path: str, config_overrides: dict | None = None) -> Any`
  - Pipeline complexo exemplo: sincroniza troca de face + voz em vídeo.
  - Parâmetros: caminhos de vídeo/imagem/modelo, overrides de configuração (opcional).
  - Retorno: saída/resultados (ex: path do vídeo processado).
- (Opcional): Métodos auxiliares para preparar dados, validar inputs, etc.

**Status:** Esqueleto criado, com docstrings detalhadas e TODOs para implementação futura.

### 5. `pipeline_manager.py`

#### Análise Pré-Código
**Responsabilidades:**
- Registrar pipelines (sequências de funções/etapas de processamento) que podem ser dinâmicos ou pré-definidos.
- Fornecer mecanismos para recuperar pipelines pelo nome.
- Permitir listar pipelines registrados.
- Tornar fácil a composição, alteração ou extensão dos pipelines (útil para customização e experimentação).

**Classe Principal:** PipelineManager

**Métodos Principais:**
- `__init__()`
  - Inicializa o gerenciador de pipelines e armazena o registro.
- `register_pipeline(name: str, steps: list[callable]) -> None`
  - Registra um novo pipeline sob um nome específico.
  - Parâmetros: nome do pipeline e lista ordenada de etapas (funções/callables).
- `get_pipeline(name: str) -> list[callable]`
  - Retorna a lista de etapas de processamento associada ao pipeline.
  - Parâmetros: nome do pipeline.
- `list_pipelines() -> list[str]`
  - Retorna os nomes de todos os pipelines registrados.
- (Opcional): Métodos para remover ou atualizar pipelines.

**Status:** Esqueleto criado, com docstrings detalhadas e TODOs para implementação futura.

---

## Progresso e Próximos Passos
- Estrutura de diretórios e arquivos principais do core criada.
- Cada componente do core está documentado e pronto para implementação incremental.
- O README será atualizado a cada novo módulo/código criado, centralizando explicação e análise de arquitetura.

---

## Como contribuir
1. Siga a estrutura de diretórios proposta.
2. Documente cada novo módulo com docstrings e comentários claros.
3. Atualize este README com explicação e análise de cada novo componente.

---

## Licença
(Escolha e preencha a licença apropriada para o projeto, ex: MIT, Apache 2.0, GPLv3, etc.)

---

## Sumário Final: Skeleton do Módulo core (`src/visiovox/core/`)

### 1. Planejamento e Alinhamento Arquitetural
O esqueleto desenvolvido para o módulo core está rigorosamente alinhado à Seção 5.1 do Documento de Design Arquitetural da VisioVox Fusion. Cada arquivo e classe implementa funções essenciais de orquestração, configuração, logging, gerenciamento de recursos e definição de pipelines dinâmicos, compondo a espinha dorsal da plataforma.

### 2. Arquivos e Suas Responsabilidades

| Arquivo              | Classe/Função(s)     | Responsabilidade Central                                                                 |
|----------------------|----------------------|-----------------------------------------------------------------------------------------|
| config_manager.py    | ConfigManager        | Gerenciar e centralizar as configurações (YAML, env), com suporte a overrides e acesso tipado. |
| logger_setup.py      | setup_logging        | Configurar o sistema de logging unificado e estruturado (console, arquivo, JSON).        |
| resource_manager.py  | ResourceManager      | Gerenciar modelos, cache/LRU, VRAM, e recursos computacionais.                           |
| orchestrator.py      | Orchestrator         | Orquestrar a execução de pipelines de processamento, coordenando módulos e recursos.     |
| pipeline_manager.py  | PipelineManager      | Registrar, listar e recuperar pipelines dinâmicos ou pré-definidos.                      |
| __init__.py          | (importação)         | Facilitar a importação de todos os componentes principais do core.                       |

### 3. Padrões, Convenções e Qualidade
- **Type Hints:** Todos os métodos utilizam type hints explícitos, promovendo segurança de tipos e integração fluida com ferramentas como linters e IDEs modernos.
- **Docstrings:** Todas as classes e métodos possuem docstrings detalhadas no estilo Google/reStructuredText, documentando claramente o propósito, parâmetros e retornos.
- **Extensibilidade:** O design esquelético facilita expansão incremental: cada componente pode ser implementado, testado e evoluído independentemente.
- **Boa Prática Python:** O `__init__.py` centraliza as importações públicas, favorecendo importação limpa e manutenção modular do sistema.

### 4. Pontos de Destaque
- **ConfigManager** já prevê acesso tipado (`get_str`, `get_int`, `get_bool`) e suporte a múltiplas fontes.
- **ResourceManager** já considera cache de modelos e awareness de recursos computacionais.
- **Orchestrator** prevê execução tanto de pipelines genéricos quanto pipelines complexos específicos (ex: face+voz em vídeo).
- **PipelineManager** permite registro flexível de sequências de etapas, fundamental para modularidade.
- **Logging** centralizado pode ser facilmente customizado por configuração.

### 5. Próximos Passos Sugeridos
- Implementar lógica concreta de cada método, começando pelo ConfigManager (leitura YAML/env), seguido do logger.
- Integrar com módulos funcionais (`media_ingestion`, `scene_analysis` etc.), conforme detalhado no documento.
- Testes unitários para cada componente do core (exemplo: `tests/unit/core/test_config_manager.py`).
- Ajustar e refinar pipelines no PipelineManager e Orchestrator conforme surgirem novos fluxos e requisitos do sistema.

### 6. Estrutura Final dos Arquivos (`src/visiovox/core/`):

```
src/visiovox/core/
├── __init__.py
├── config_manager.py
├── logger_setup.py
├── resource_manager.py
├── orchestrator.py
└── pipeline_manager.py
```

O módulo core está arquitetado para servir como fundação sólida e flexível para toda a VisioVox Fusion. 

---

## PROMPT PADRÃO PARA IMPLEMENTAÇÃO DE SKELETON DE UM MÓDULO

[Projeto: VisioVox Fusion — Skeleton do Módulo <nome_do_módulo>]

Você atuará como Arquiteto de Software Sênior e Desenvolvedor Python para o Projeto VisioVox Fusion.

Seu objetivo neste chat é criar o código skeleton completo do módulo `<nome_do_módulo>` (localizado em `src/visiovox/<diretório>/<nome_do_módulo>/`), seguindo a mesma lógica de construção adotada no skeleton do core, baseada no documento de arquitetura oficial do projeto.

**Processo obrigatório para cada arquivo/classe do módulo:**

1. **Análise Pré-Código:**
   - Reitere as principais responsabilidades do(s) componente(s) a serem implementados.
   - Liste as classes principais e seus métodos, detalhando o propósito, parâmetros (com type hints), e tipo de retorno.

2. **Geração do Código:**
   - Implemente o esqueleto das classes e métodos, com type hints completos, docstrings detalhadas (Google ou reStructuredText).
   - Inclua as importações necessárias.
   - Use `pass` ou comentários-todo onde aplicável.

3. **Notas e Recomendações:**
   - Traga quaisquer observações relevantes sobre dependências, integração futura, possíveis extensões ou padrões especiais para o módulo.

4. **Resumo Final e Checagem das Responsabilidades:**
   - Confirme que o esqueleto cobre as responsabilidades do módulo conforme a arquitetura.
   - Liste os arquivos/classe/métodos criados e suas funções.
   - Ressalte pontos de atenção para a próxima etapa de implementação.

5. **Sumário Final do Skeleton do Módulo `<nome_do_módulo>`:**
   - Apresente um sumário objetivo dos pontos centrais e próximos passos recomendados para este módulo.

**Exemplo de chamada para este prompt (adapte o nome do módulo):**
[Projeto: VisioVox Fusion — Skeleton do Módulo media_ingestion]

Este chat é dedicado à estruturação do skeleton do módulo media_ingestion do Projeto VisioVox Fusion, localizado em src/visiovox/modules/media_ingestion/, conforme definido na arquitetura aprovada.

Por favor, siga o processo:

Análise Pré-Código (responsabilidades, classes/métodos e type hints);

Geração do Código;

Notas e Recomendações;

Resumo Final e Checagem das Responsabilidades;

Sumário Final do Skeleton do Módulo media_ingestion.

Pronto para iniciar? =

---

## SUGESTÕES DE MÓDULOS-CHAVE E SEUS PROMPTS DE ABERTURA

Você pode abrir um novo chat para cada um dos seguintes, adaptando o nome do módulo no prompt padrão acima:

1. **media_ingestion**  
   - `src/visiovox/modules/media_ingestion/`
   - Responsável por: Carregar, validar e pré-processar mídias (imagens, vídeos, áudio).

2. **scene_analysis**
   - `src/visiovox/modules/scene_analysis/`
   - Responsável por: Detecção de faces, extração de landmarks, segmentação.

3. **facial_processing**
   - `src/visiovox/modules/facial_processing/`
   - Responsável por: Face swap, aprimoramento, edição facial.

4. **voice_processing**
   - `src/visiovox/modules/voice_processing/`
   - Responsável por: Conversão e manipulação de voz.

5. **visual_generation**
   - `src/visiovox/modules/visual_generation/`
   - Responsável por: Geração de imagens sintéticas (ex: StyleGANEX).

6. **multimodal_sync**
   - `src/visiovox/modules/multimodal_sync/`
   - Responsável por: Sincronização de face/voz (lip sync etc).

7. **live_stream**
   - `src/visiovox/modules/live_stream/`
   - Responsável por: Orquestração de pipelines ao vivo, gerenciamento de streaming.

8. **model_management**
   - `src/visiovox/modules/model_management/`
   - Responsável por: Download, verificação, cache e carregamento de modelos.

9. **apis** (API FastAPI)
   - `src/visiovox/apis/`
   - Responsável por: Endpoints, routers, schemas Pydantic.

10. **cli**
    - `src/visiovox/cli/`
    - Responsável por: Interface de linha de comando.

11. **gui**
    - `src/visiovox/gui/`
    - Responsável por: Interface gráfica desktop.

---

## Resumo Visual para Organização Modular
Projeto VisioVox Fusion
│
├── Skeleton do Core (este chat)
│
├── [Novo Chat] Skeleton do Módulo media_ingestion
├── [Novo Chat] Skeleton do Módulo scene_analysis
├── [Novo Chat] Skeleton do Módulo facial_processing
├── [Novo Chat] Skeleton do Módulo voice_processing
├── [Novo Chat] Skeleton do Módulo visual_generation
├── [Novo Chat] Skeleton do Módulo multimodal_sync
├── [Novo Chat] Skeleton do Módulo live_stream
├── [Novo Chat] Skeleton do Módulo model_management
├── [Novo Chat] Skeleton do Módulo apis
├── [Novo Chat] Skeleton do Módulo cli
└── [Novo Chat] Skeleton do Módulo gui

**(Cada novo chat recebe um prompt inicial, segue o processo padrão, e gera um sumário final do skeleton do módulo.)**

---

Se quiser, já posso sugerir prompts específicos para os próximos módulos que você pretende abrir!
Caso queira um template `.md` para salvar e reaproveitar, também posso gerar.

**Só me dizer por qual módulo quer começar!**

---

## Roadmap Sugerido de Skeletons — VisioVox Fusion

Vou propor uma ordem que facilita a integração e os testes progressivos dos módulos, sempre detalhando e validando com você a cada etapa:

1. **Módulo media_ingestion**  
   *Motivo:* Tudo começa com ingestão de dados (imagens, vídeos, áudio). É a base para os pipelines de processamento.

2. **Módulo scene_analysis**  
   *Motivo:* Após ingestão, o sistema precisa identificar o que processar (faces, landmarks, regiões).

3. **Módulo facial_processing**  
   *Motivo:* Face swap, enhancement, etc., são centrais ao propósito do projeto.

4. **Módulo voice_processing**  
   *Motivo:* Permite unir o facial com o vocal para experiências multimodais.

5. **Módulo multimodal_sync**  
   *Motivo:* Sincronização entre imagem e áudio, essencial para deepfakes realistas.

6. **Módulo visual_generation**  
   *Motivo:* Geração avançada, como StyleGANEX, complementa a edição facial.

7. **Módulo live_stream**  
   *Motivo:* Permite aplicações em tempo real, streamings e testes rápidos.

8. **Módulo model_management**  
   *Motivo:* Download, cache, verificação e gerenciamento de modelos de IA.

9. **Módulo(s) de Interface (apis, cli, gui)**  
   *Motivo:* Expõe a plataforma via API web, CLI ou GUI para o usuário.

---

## Sumário do Skeleton do Módulo `facial_processing`

### 1. Análise Pré-Código
- **Responsabilidades Principais:**
  - Troca de faces (face swap) em imagens ou vídeos.
  - Aprimoramento de faces (face enhancement) usando modelos como GFPGAN, CodeFormer.
  - Aprimoramento de quadros completos (frame enhancement) — para vídeos ou imagens inteiras.
  - Edição facial: efeitos, ajustes, filtros, manipulações criativas.
- **Arquivos Criados:**
  - `face_swapper.py`: Abstrações e implementação exemplo para face swap.
  - `face_enhancer.py`: Abstrações e implementação exemplo para face enhancement.
  - `frame_enhancer.py`: Abstrações e implementação exemplo para aprimoramento de quadros.
  - `face_editor.py`: Abstrações e implementação exemplo para edição facial avançada.
- **Classes Principais:**
  - Abstrações: `BaseFaceSwapper`, `BaseFaceEnhancer`, `BaseFrameEnhancer`, `BaseFaceEditor`
  - Implementações: `InSwapperFaceSwapper`, `GFPGANFaceEnhancer`, `RealESRGANFrameEnhancer`, `StyleGANEXFaceEditor`

### 2. Geração do Código
- Todos os arquivos possuem classes base abstratas e implementações concretas de exemplo.
- Métodos com type hints, docstrings detalhadas e comentários TODO para implementação futura.

### 3. Notas e Recomendações
- **Extensibilidade:** Pronto para múltiplos backends, fácil adicionar novas implementações concretas.
- **Integração:** Todas as classes aceitam `ConfigManager | dict`, facilitando integração com o core.
- **Dependências:** Ao implementar, adicionar imports específicos de cada framework (insightface, gfpgan, realesrgan, styleganex).
- **Padronização:** O padrão de métodos facilita composição de pipelines no Orchestrator.

### 4. Resumo Final e Checagem das Responsabilidades
- **Cobertura Arquitetural:** O skeleton cobre todas as responsabilidades do módulo `facial_processing`, como descrito no documento de arquitetura:
  - Troca de faces (`face_swapper.py`)
  - Aprimoramento facial (`face_enhancer.py`)
  - Aprimoramento de quadros (`frame_enhancer.py`)
  - Edição facial criativa (`face_editor.py`)
- **Interface Clean:** Métodos abstratos e concretos garantem plugabilidade de novos modelos.
- **Pronto para Integração:** Estrutura pronta para ser usada pelo Orchestrator e integrada ao pipeline geral.
- **Docstrings e Type Hints:** Completos em todas as classes/métodos.

### 5. Sumário Final do Skeleton do Módulo `facial_processing`
- **Arquivos criados:**
  - `face_swapper.py`
  - `face_enhancer.py`
  - `frame_enhancer.py`
  - `face_editor.py`
- **Responsabilidades:** Troca, aprimoramento e edição de faces/quadros, entregando resultados padronizados para o pipeline.
- **Expansível:** Pronto para novos modelos, integrações e formatos de saída.
- **Pronto para Implementação:** Só preencher as lógicas de cada método e integrar testes.

---

## Sumário do Skeleton do Módulo `voice_processing`

### 1. Análise Pré-Código
- **Responsabilidades Principais:**
  - Conversão de voz baseada em modelos (exemplo: RVC — Retrieval-based Voice Conversion).
  - Aplicação de efeitos em áudio (reverb, equalização, filtros, etc.).
  - Processamento vocal paramétrico (alteração de pitch, timbre, gênero).
  - Interfaces padronizadas para cada etapa do pipeline vocal.
  - Abstrações via ABC para facilitar futuras expansões/implementações.
- **Arquivos Criados:**
  - `rvc_processor.py`: Conversor de voz.
  - `effects_processor.py`: Efeitos de áudio.
  - `pitch_processor.py`: Processamento de pitch.
- **Classes Principais:**
  - Abstrações: `BaseVoiceConverter`, `BaseVoiceEffectsProcessor`, `BasePitchProcessor`
  - Implementações: `RVCVoiceConverter`, `DefaultVoiceEffectsProcessor`, `DefaultPitchProcessor`

### 2. Geração do Código
- Todos os arquivos possuem classes base abstratas e implementações concretas de exemplo.
- Métodos com type hints, docstrings detalhadas e comentários TODO para implementação futura.

### 3. Notas e Recomendações
- **Extensibilidade:** Toda interface é uma ABC, permitindo múltiplas implementações (futuro: suporte a outros frameworks além de RVC).
- **Integração:** Todos recebem `ConfigManager` ou `dict`, mantendo padrão de integração core-modules.
- **Flexibilidade de Entrada/Saída:** Use sempre formatos genéricos (`Any`), mas recomenda-se padronizar (numpy array, path para .wav, etc.) e documentar no futuro.
- **Bibliotecas recomendadas:** librosa, soundfile, torchaudio, pydub (e compatíveis).
- **Testabilidade:** Estrutura pronta para testes unitários/mocks.

### 4. Resumo Final e Checagem das Responsabilidades
- **Cobertura Arquitetural:**
  - Conversão vocal (RVC e futuros).
  - Aplicação de efeitos (reverb, equalizador, etc.).
  - Processamento de pitch e timbre.
  - ABCs garantem padronização e plugabilidade.
- **Pronto para integração incremental e fácil documentação.**
- **Arquivos/criação:**
  - `rvc_processor.py`: Conversor de voz.
  - `effects_processor.py`: Efeitos de áudio.
  - `pitch_processor.py`: Processamento de pitch.
  - Todos com classes abstratas (interface) e padrão para implementação default.

### 5. Sumário Final do Skeleton do Módulo `voice_processing`
- **Estrutura preparada para múltiplos backends de conversão e efeitos vocais.**
- **Design modular:** Fácil expandir para novos modelos/bibliotecas.
- **Padronização:** Docstrings Google, type hints, métodos flexíveis.
- **Pronto para testes, integração com o Orchestrator/core e extensões futuras.**

---

## Sumário do Skeleton do Módulo `multimodal_sync`

### 1. Análise Pré-Código
- **Responsabilidades Principais:**
  - Sincronização multimodal entre frames faciais (vídeo/imagem) e áudio (voz).
  - Lip sync automático (ajuste de boca/lábios para o áudio).
  - (Opcional/futuro) Sincronização gestual/facial — expressão, cabeça etc.
  - Interfaces padronizadas para uso em pipelines (output: frames/vídeo sincronizados).
  - Pronto para expansão futura (novos métodos/modelos de sincronização).
- **Arquivos Criados:**
  - `lip_syncer.py`: Base + implementação LatentSync.
  - `gesture_syncer.py`: Base + implementação básica.
  - `__init__.py`: Exposição dos componentes principais.
- **Principais classes e métodos:**
  - `BaseLipSyncer.sync`, `LatentSyncLipSyncer.sync`
  - `BaseGestureSyncer.sync_gestures`, `DefaultGestureSyncer.sync_gestures`

### 2. Geração do Código
- Todas as classes base são abstratas (ABC), garantindo contratos robustos e expansibilidade.
- Implementações concretas para lip sync (LatentSync) e gestos (stub/futuro).
- Métodos com type hints, docstrings detalhadas e comentários TODO para implementação futura.

### 3. Notas e Recomendações
- **Extensibilidade:** O uso de classes base abstratas (ABC) garante que novos métodos/modelos de sincronização possam ser adicionados sem alterar o pipeline principal.
- **Dependências:** A dependência em frameworks como LatentSync, motion capture, etc., pode ser gerenciada via wrappers/integrations no futuro.
- **Integração:** O módulo está pronto para receber frames e áudio dos módulos anteriores (facial_processing, voice_processing).
- **Entrada/Saída:** Recomenda-se padronizar o formato de entrada (np.ndarray para frames, path ou waveform para áudio) e documentar no início da implementação.

### 4. Resumo Final e Checagem das Responsabilidades
- **Cobertura Arquitetural:** O skeleton cobre todas as funções-chave de sincronização multimodal: lip sync (LatentSync) e gestos (opcional/futuro), alinhado à arquitetura VisioVox Fusion.
- **Interface ABC:** Garante contratos robustos e expansibilidade para novos backends e tecnologias.
- **Integração:** Pronto para uso incremental em pipelines e testes unitários.

### 5. Sumário Final do Skeleton do Módulo `multimodal_sync`
- **Arquivos criados:**
  - `lip_syncer.py` (Base + implementação LatentSync)
  - `gesture_syncer.py` (Base + implementação básica)
  - `__init__.py` (exposição dos componentes principais)
- **Responsabilidades cobertas:**
  - Sincronização multimodal (face-voz), com foco inicial em lip sync.
  - Infraestrutura para gestos/expressão (expansível).
- **Pronto para:**
  - Implementação incremental (ex: adicionar wrappers para novos frameworks).
  - Testes unitários, integração com orquestrador e pipeline manager.
- **Próximos passos recomendados:**
  - Definir formatos padrão de entrada/saída (docstring ou dataclasses).
  - Integrar ao pipeline de vídeo e áudio real do sistema.
  - Implementar e validar a chamada real ao LatentSync e frameworks de gestos (quando disponíveis). 

## Sumário do Skeleton do Módulo `live_stream`

### 1. Análise Pré-Código
- **Responsabilidades Principais:**
  - Orquestrar a execução de pipelines multimodais em tempo real (ao vivo), via webcam, arquivo, RTMP, etc.
  - Gerenciar captura, processamento e transmissão de vídeo/áudio em tempo real.
  - Integrar com frameworks de streaming como OpenCV, GStreamer, WebRTC, FFmpeg, aiortc.
  - Gerenciar threads/processos para ingest, processamento e output em paralelo ou assíncrono.
  - Fornecer hooks/callbacks para monitoramento (status, logs, métricas de desempenho).
  - Facilitar expansão futura para novos protocolos/backends.
- **Arquivos Criados:**
  - `stream_orchestrator.py`: Orquestrador de streaming ao vivo (base + implementação padrão).
  - `stream_worker.py`: Worker de streaming (base + implementação OpenCV).
  - `__init__.py`: Exposição das interfaces principais do módulo.
- **Classes Principais:**
  - Abstrações: `BaseLiveStreamOrchestrator`, `BaseStreamWorker`
  - Implementações: `DefaultLiveStreamOrchestrator`, `OpenCVStreamWorker`

### 2. Geração do Código
- Todas as classes base são abstratas (ABC), garantindo contratos robustos e expansibilidade.
- Implementações concretas para orquestração e worker OpenCV.
- Métodos com type hints, docstrings detalhadas e comentários TODO para implementação futura.

### 3. Notas e Recomendações
- **Extensibilidade:** O uso de ABCs permite plugar novos protocolos/backends (ex: GStreamer, WebRTC) sem alterar a interface pública.
- **Integração:** O orquestrador está pronto para ser consumido pelo PipelineManager/Core e integrado via API (ex: endpoints de "iniciar/encerrar live" na API FastAPI).
- **Concorrência:** Estrutura pronta para paralelismo, threads ou processamento assíncrono, a depender da estratégia de implementação futura (threading, multiprocessing, asyncio).
- **Testabilidade:** Workers podem ser mockados e hooks testados independentemente.
- **Input/Output:** Métodos aceitam input_source flexível (str, int, RTMP, etc), essencial para pipelines multimodais em diferentes ambientes.

### 4. Resumo Final e Checagem das Responsabilidades
- **Cobertura Arquitetural:**
  - Orquestração de pipelines em tempo real, gerenciamento de ciclo de vida do stream, separação worker/orchestrator, integração flexível de pipelines e hooks de monitoramento estão contempladas.
- **Padronização e Extensibilidade:**
  - Uso de classes base abstratas e contratos padronizados para métodos fundamentais.
  - Facilidade para adicionar novos protocolos/backends no futuro.
- **Pronto para Integração e Testes:**
  - O orquestrador pode ser instanciado por qualquer outro módulo/pipeline do VisioVox.
  - Workers podem ser trocados conforme o backend de streaming desejado.

### 5. Sumário Final do Skeleton do Módulo `live_stream`
- **Arquivos criados:**
  - `__init__.py`
  - `stream_orchestrator.py`
  - `stream_worker.py`
- **Responsabilidades Centrais:**
  - Orquestração de pipelines em tempo real, gerenciamento de threads/workers, integração fácil com diferentes protocolos de streaming, hooks para monitoramento e expansibilidade para múltiplos backends.
- **Pontos de Atenção:**
  - Ao implementar, decidir o modelo de concorrência (threads, processes, asyncio) mais apropriado para cada backend.
  - Documentar claramente o formato esperado de entrada/saída (frames, áudio, callbacks).
  - Ao integrar com a API, prever hooks para start/stop remoto do stream.
  - Adicionar testes unitários para orquestrador e workers. 

---

## Exemplo de Uso dos Módulos

### Exemplo: Uso do Orquestrador de Streaming ao Vivo
```python
from visiovox.modules.live_stream import DefaultLiveStreamOrchestrator, OpenCVStreamWorker

# Configuração (pode ser um dict ou ConfigManager)
config = {...}

# Pipeline de processamento (stub/exemplo)
def pipeline(frame):
    # Processa o frame
    return frame

# Instancia o orquestrador
gorchestrator = DefaultLiveStreamOrchestrator(config)

# Inicia o streaming ao vivo (ex: webcam 0 para arquivo de saída)
gorchestrator.start_stream(0, "output.mp4", pipeline)

# Para o streaming
# orchestrator.stop_stream()
```

### Exemplo: Uso do Módulo de Ingestão de Mídia
```python
from visiovox.modules.media_ingestion.loader import BaseMediaLoader, DefaultMediaLoader

loader = DefaultMediaLoader(config)
media = loader.load("input.mp4")
```

### Exemplo: Uso do Módulo de Processamento Facial
```python
from visiovox.modules.facial_processing.face_swapper import InSwapperFaceSwapper

swapper = InSwapperFaceSwapper(config)
result = swapper.swap(source_face, target_frame, model_name="inswapper_128")
```

### Exemplo: Uso do Módulo de Geração Visual
```python
from visiovox.modules.visual_generation import StyleGANEXVisualGenerator

generator = StyleGANEXVisualGenerator(model_path, config)
image = generator.generate({"latent": ..., "attributes": ...})
```

---

## Template para Documentação de Novos Módulos

```markdown
## Sumário do Skeleton do Módulo `<nome_do_módulo>`

### 1. Análise Pré-Código
- **Responsabilidades Principais:**
  - <Descreva as principais funções e objetivos do módulo>
- **Arquivos Criados:**
  - `<arquivo1.py>`: <descrição>
  - `<arquivo2.py>`: <descrição>
  - ...
- **Classes Principais:**
  - Abstrações: `<BaseClass1>`, `<BaseClass2>`
  - Implementações: `<ImplClass1>`, `<ImplClass2>`

### 2. Geração do Código
- Todas as classes base são abstratas (ABC), garantindo contratos robustos e expansibilidade.
- Implementações concretas para as principais funções do módulo.
- Métodos com type hints, docstrings detalhadas e comentários TODO para implementação futura.

### 3. Notas e Recomendações
- **Extensibilidade:** <Como expandir o módulo para novos backends, protocolos, etc>
- **Integração:** <Como o módulo se integra ao core/pipelines/infraestrutura>
- **Testabilidade:** <Como testar/mocar as interfaces>
- **Input/Output:** <Formatos esperados, recomendações de documentação>

### 4. Resumo Final e Checagem das Responsabilidades
- **Cobertura Arquitetural:** <Confirmação de que o skeleton cobre as funções-chave do módulo>
- **Padronização e Extensibilidade:** <Uso de ABCs, contratos, etc>
- **Pronto para Integração e Testes:** <Como o módulo pode ser integrado/testado>

### 5. Sumário Final do Skeleton do Módulo `<nome_do_módulo>`
- **Arquivos criados:**
  - `<arquivo1.py>`
  - `<arquivo2.py>`
- **Responsabilidades Centrais:** <Resumo das funções principais>
- **Pontos de Atenção:** <Dicas para implementação futura, concorrência, formatos, etc>

### Exemplo de Uso
```python
from visiovox.modules.<nome_do_módulo> import <ClassePrincipal>

obj = <ClassePrincipal>(config)
resultado = obj.<metodo_principal>(...)
```
```

---

# Fim do Template e Exemplos 

---

## Mudanças Recentes e Padronizações (2025-05-21)

- **Padronização dos Routers:**
  - Todos os routers de domínio (media, facial, voice, visual, scene, multimodal, live, model management) agora usam apenas schemas genéricos (`MediaProcessRequest`, `MediaProcessResponse`, `TaskStatusResponse`, `ErrorResponse`, `PaginatedResponse`).
  - Prefixos dos routers removidos dos próprios APIRouter e definidos apenas no `main.py` para evitar duplicidade de rotas.
  - Imports e handlers ajustados para não depender de schemas inexistentes ou específicos.
- **Fluxo de Testes Automatizados:**
  - Testes automatizados com `pytest` cobrem todos os principais endpoints e domínios.
  - Mocks do Celery aplicados globalmente para impedir conexões reais durante os testes.
  - Ambiente Docker pronto para desenvolvimento incremental: basta subir os containers e rodar os testes sem rebuilds desnecessários.
- **Cobertura de Testes:**
  - Cobertura de código aumentada para 76%.
  - Relatório HTML de cobertura gerado em `scripts/coverage_html`.
- **Troubleshooting:**
  - Se algum teste tentar conectar ao Celery real, garanta que o mock global de `celery.app.task.Task.apply_async` está ativo no teste.
  - Para adicionar novos domínios, siga o padrão de schemas genéricos e inclua mocks no arquivo de testes correspondente.

---

## Testes Automatizados

### Como rodar os testes

1. Suba os containers:
   ```bash
   docker compose up -d
   ```
2. Execute os testes dentro do container da API:
   ```bash
   docker compose exec api poetry run pytest --cov=src
   ```
3. O relatório de cobertura será gerado em `scripts/coverage_html`.

### Estrutura dos testes
- Todos os endpoints principais são testados via `TestClient` do FastAPI.
- Mocks do Celery garantem que nenhum teste dependa de infraestrutura externa.
- Exemplos de testes podem ser encontrados em `tests/apis/test_router.py`.

---

# Fim do Template e Exemplos 
```

---

## Progresso Atual — Última Atualização: 21/05/2025

### Onde estamos no projeto
- **Estrutura de diretórios e arquivos skeleton** criada para todos os módulos core e principais módulos funcionais, conforme o documento de arquitetura.
- **Skeletons completos** (com docstrings, type hints, pontos de extensão e análise pré-código) já implementados para:
  - Módulo core (`src/visiovox/core/`): ConfigManager, Logger, ResourceManager, Orchestrator, PipelineManager.
  - Módulos funcionais: `media_ingestion`, `scene_analysis`, `facial_processing`, `voice_processing`, `multimodal_sync`, `visual_generation`, `live_stream`, `model_management` (todos com classes base, exemplos de implementação e docstrings detalhadas).
- **Template de documentação** para novos módulos e exemplos de uso já incluídos no README.
- **Padronização dos routers e schemas** para APIs, com testes automatizados e cobertura de código documentada.
- **Ambiente Docker e testes automatizados** prontos para desenvolvimento incremental.

### Próximo passo sugerido
- Iniciar a implementação concreta dos métodos dos módulos core, começando pelo `ConfigManager` (leitura YAML/env), seguido do `Logger`.
- Integrar os módulos funcionais ao pipeline principal via Orchestrator e PipelineManager.
- Expandir testes unitários para cobrir integrações entre módulos.