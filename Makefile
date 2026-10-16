COMPOSE = docker compose -f infra/docker-compose.yml --env-file .env
Q ?= Q01

.PHONY: env up down ps logs ingest ask ask-local rebuild test

env:            ## generate .env secrets (safe to re-run)
	uv run python scripts/init_env.py

up: env         ## build and start Neo4j, Helix MCP and Langfuse
	$(COMPOSE) up -d --build --wait

down:           ## stop everything (data volumes are kept)
	$(COMPOSE) down

ps:             ## service status
	$(COMPOSE) ps --format '{{.Service}}: {{.Status}}'

logs:           ## follow Helix MCP and Langfuse logs
	$(COMPOSE) logs -f helix-mcp langfuse-web langfuse-worker

ingest:         ## load the Orbisa corpus into the Helix graph
	$(COMPOSE) run --rm helix-ingest

ask:            ## ask a ground-truth question in Docker: make ask Q=Q07
	$(COMPOSE) run --rm agent --id $(Q)

ask-local:      ## same, from the host venv: make ask-local Q=Q07
	uv run python -m clients.agent --id $(Q)

rebuild:        ## rebuild the Helix image after code changes and restart the MCP server
	$(COMPOSE) up -d --build --wait helix-mcp

test:
	uv run pytest -q
