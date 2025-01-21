up:
	docker compose up -d

down:
	docker compose down && docker network prune --force

restart: down up


logs:
	docker compose logs -f

logs-web:
	docker compose logs -f web

logs-db:
	docker compose logs -f db

logs-bot:
	docker compose logs -f bot


console-web:
	docker exec -it django_app sh

remove-containers:
	docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -q) && docker system prune -a && docker volume rm $(docker volume ls -q)