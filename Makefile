# Physics Derivation Graph
# https://allofphysics.com
# Ben Payne, 2026

# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

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

CONTAINER_TAG=latest-$(this_arch)

DOCKER_OR_PODMAN=docker
#DOCKER_OR_PODMAN=podman

# .PHONY is special target used to declare that a target name does not correspond to an actual file to be built.
.PHONY: help clean webserver typehints flake8 pylint doctest mccabe

# todo: $(DOCKER_OR_PODMAN) kill $(docker ps -q); make up

# `launch_webserver` depends on the image `allofphysicscom-flask` being available so that `black` can run
launch_webserver:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi;
	docker ps
	if [ `docker ps | wc -l` -gt 1 ]; then \
		docker kill $$(docker ps -q); \
		fi
	docker ps
	docker run -it --rm --entrypoint /bin/bash \
            -v `pwd`:/scratch allofphysicscom-flask:latest-$(this_arch) -c 'black /scratch/flask/*.py'
	$(DOCKER_OR_PODMAN) compose up --build --force-recreate --remove-orphans --detach

launch_webserver_monitor:
	if (! docker stats --no-stream ); then  open /Applications/Docker.app; while (! docker stats --no-stream ); do    echo "Waiting for Docker to launch...";  sleep 1; done; fi; 
	docker ps
	if [ `docker ps | wc -l` -gt 1 ]; then \
	       	docker kill $$(docker ps -q); \
		fi
	docker ps
	docker run -it --rm --entrypoint /bin/bash \
	    -v `pwd`:/scratch allofphysicscom-flask:latest-$(this_arch) -c 'black /scratch/flask/*.py'
	$(DOCKER_OR_PODMAN) compose up --build --force-recreate --remove-orphans

down:
	# https://docs.docker.com/compose/reference/down/
	$(DOCKER_OR_PODMAN) compose down --volumes --remove-orphans

kill:
	docker ps
	docker kill $$(docker ps -q)


# keep the conf folder since that has the configuration
# keep plugin folder since that has apocalypse
delete_neo4j_file:
	rm -rf neo4j_pdg/data/
	rm -rf neo4j_pdg/logs/

# This will remove:
#  - all stopped containers
#  - all networks not used by at least one container
#  - all dangling images
#  - unused build cache
clear_containers:
	docker system prune


# EOF
