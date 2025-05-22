# Módulo APIs — VisioVox Fusion

## Visão Geral
- Routers RESTful para todos os domínios (media, facial, voice, visual, scene, multimodal, live, models).
- Tasks Celery plugáveis para cada domínio, com update_state e logging.
- Healthcheck detalhado em `/healthz`.
- Schemas Pydantic padronizados e incrementais.

## Exemplos de Uso
- Upload de imagem/vídeo via `/scene_analysis/analyze`.
- Polling incremental de status via `/scene_analysis/status/{task_id}`.
- Healthcheck: `/healthz` retorna status de API, Celery, Redis, modelos, GPU.

## Dicas de Expansão
- Para adicionar novo domínio, crie router, schemas e task Celery seguindo o padrão.
- Use campos opcionais nos schemas para evolução incremental.
- Plugue módulos reais no pipeline e preencha campos conforme disponibilidade.

## Troubleshooting
- Use logs detalhados (task_id, params, traceback).
- Healthcheck detalhado facilita troubleshooting de dependências.
- FAQ disponível em cada módulo.

## Integração com Frontend
- API pronta para consumo via Axios/Fetch.
- Suporte a upload, polling, overlays, feedback incremental.

## Observabilidade
- Logging estruturado em todos os endpoints/tasks.
- Pronto para Sentry (exceções) e Prometheus (métricas).

---

**Documentação viva, incremental e pronta para onboarding de devs, QA e clientes!** 