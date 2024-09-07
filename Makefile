
# todo: docker kill $(docker ps -q); make up

up_monitor:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi; 
	docker ps
	if [ `docker ps | wc -l` -gt 1 ]; then \
	       	docker kill $$(docker ps -q); \
		fi
	docker ps
	docker compose up --build --force-recreate --remove-orphans

up:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi;
	docker ps
	if [ `docker ps | wc -l` -gt 1 ]; then \
		docker kill $$(docker ps -q); \
		fi
	docker ps
	docker compose up --build --force-recreate --remove-orphans --detach


down:
	docker compose down


kill:
	docker ps
	docker kill $$(docker ps -q)


# This will remove:
#  - all stopped containers
#  - all networks not used by at least one container
#  - all dangling images
#  - unused build cache
clear:
	docker system prune


# EOF
