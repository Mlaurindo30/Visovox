# FAQ & HowTo — Módulo scene_analysis

## Como expandir schemas?
- Basta adicionar novos campos opcionais nos schemas Pydantic (`src/visiovox/apis/schemas.py`).
- Exemplo: para adicionar "emotion" em atributos, inclua em `FaceAttributes`.
- Campos opcionais não quebram clientes antigos.

## Como plugar um novo detector/landmark/segmenter?
- Importe sua classe no `pipeline_manager.py`.
- Instancie e chame no método `run_pipeline` conforme o parâmetro em `params`.
- Exemplo:
  ```python
  if params.get("detect_mode") == "MediaPipe":
      detector = MediaPipeFaceDetector(...)
  ```
- Preencha o campo correspondente no resultado (ex: `landmarks`, `masks`).

## Como testar upload e status?
- Use o script de testes automatizados ou o Swagger (`/docs`).
- Exemplo Pytest:
  ```python
  def test_analyze_scene_image():
      with open("tests/assets/sample.jpg", "rb") as img:
          response = client.post(
              "/scene_analysis/analyze",
              files={"file": ("sample.jpg", img, "image/jpeg")},
              data={"media_type": "image", "params": '{"detect_mode": "YOLOFace"}'}
          )
      assert response.status_code == 200
  ```

## Como simular estados do Celery?
- Use monkeypatch no Pytest para simular estados (queued, success, failure).
- Veja exemplos em `tests/apis/test_scene_analysis.py`.

## Como debugar erros?
- Verifique logs do Celery e FastAPI (task_id, payload, traceback).
- Use o campo `detail` do response para mensagens de erro detalhadas.

## Como integrar com frontend?
- Envie imagem/vídeo via multipart/form-data.
- Faça polling em `/scene_analysis/status/{task_id}` para feedback incremental.
- Exiba overlays e previews usando os campos `overlay_url`, `mask_url`.

## Como adicionar um novo campo no resultado?
- Adicione no schema, preencha no pipeline, e pronto!
- Exemplo: para embeddings, adicione `embedding: Optional[List[float]]` em `FaceDetectionResult`.

## Dicas rápidas
- Sempre use campos opcionais para evolução incremental.
- Nunca remova campos antigos: só adicione novos.
- Documente exemplos reais no README e Swagger. 