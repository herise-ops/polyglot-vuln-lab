.PHONY: up down logs smoke list

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f

smoke:
	bash scripts/smoke-test.sh

list:
	find . -maxdepth 3 -type f | sort
