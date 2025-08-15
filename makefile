docker-build:
	docker compose up --build -d

run-prod:
	uv run run_produce.py

run-cons:
	uv run run_consume.py