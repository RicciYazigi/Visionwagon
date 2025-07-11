# 🚀 Wagon X

Sistema de agentes IA basado en Vision Wagon, preparado para B2B y NSFW creators. Docker, API, YAML workflows incluidos.

## Quickstart

```bash
cp .env.example .env
docker compose up --build
./dev-utils.sh run-workflow example_workflow_eros
```

Archivos clave:
- `vision_wagon/agents/*`: Agentes IA
- `workflows/example_workflow_eros.yaml`: Ejemplo de flujo
- `config/config_multi.yaml`: Claves y entornos

Listo para extender con APIs reales (OpenAI, ElevenLabs, SD). Incluye tests, CI pipeline, y estructura para SaaS.
