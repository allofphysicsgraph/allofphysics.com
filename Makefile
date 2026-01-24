# Ben Payne
# Physics Derivation Graph
# https://allofphysics.com

# Get the machine architecture.
# On arm64 (Apple Silicon M1/M2/etc.), `uname -m` outputs "arm64".
# On amd64 (Intel), `uname -m` outputs "x86_64".
ARCH := $(shell uname -m)

ifeq ($(ARCH), arm64)
        this_arch=arm64
else ifeq ($(ARCH), x86_64)
        this_arch=amd64
else
        @echo "Unknown architecture: $(ARCH). Cannot determine if Mac is new (arm64) or old (amd64)."
endif

# todo: docker kill $(docker ps -q); make up

up_monitor:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi; 
	docker ps
	if [ `docker ps | wc -l` -gt 1 ]; then \
	       	docker kill $$(docker ps -q); \
		fi
	docker ps
	docker run -it --rm -v `pwd`:/scratch allofphysicscom-flask:latest-$(this_arch) /bin/bash -c 'for filename in /scratch/flask/*.py; do echo $$filename; done | xargs black'
	docker compose up --build --force-recreate --remove-orphans

# `up` depends on the image `allofphysicscom-flask` being available so that `black` can run
up:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi;
	docker ps
	if [ `docker ps | wc -l` -gt 1 ]; then \
		docker kill $$(docker ps -q); \
		fi
	docker ps
	docker run -it --rm --entrypoint /bin/bash \
            -v `pwd`:/scratch allofphysicscom-flask:latest-$(this_arch) -c 'black /scratch/flask/*.py'
	docker compose up --build --force-recreate --remove-orphans --detach


down:
	docker compose down


kill:
	docker ps
	docker kill $$(docker ps -q)

#docker_push:
#	docker buildx build --push --platform linux/arm64,linux/amd64 --tag benislocated/allofphysicscom-flask:latest-$(this_arch) .


# This will remove:
#  - all stopped containers
#  - all networks not used by at least one container
#  - all dangling images
#  - unused build cache
clear:
	docker system prune


# EOF
