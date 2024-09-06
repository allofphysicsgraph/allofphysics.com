
# todo: docker kill $(docker ps -q); make up

up_monitor:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi; docker compose up --build --force-recreate --remove-orphans

up:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi; docker compose up --build --force-recreate --remove-orphans --detach


down:
	docker compose down


kill:
	docker kill $(docker ps -q)


# This will remove:
#  - all stopped containers
#  - all networks not used by at least one container
#  - all dangling images
#  - unused build cache
clear:
	docker system prune

