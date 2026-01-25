
This repo is the source code for the website <https://allofphysics.com>, aka <https://derivationmap.net/>.

See [developer documentation](https://derivationmap.net/developer_documentation?referrer=github_README) after reading the [user documentation](https://derivationmap.net/user_documentation)

# How to use (for the impatient)

```bash
git clone https://github.com/allofphysicsgraph/allofphysics.com.git
cd allofphysics.com
make up
```

# Files not in this repo
You won't be able to immediately use the code because there are four files which you need to create associated with SSL certificates:
 * `certs/dhparam.pem`
 * `certs/fullchain.pem`
 * `certs/privkey.pem`
 * `.env`



The `.env` file contains three lines,
```bash
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
SECRET_KEY=
```

## build and run

```bash
docker compose up --build --remove-orphans
```
or
```bash
docker compose up --build --remove-orphans --detach
```
or
```bash
docker compose up --build --force-recreate --remove-orphans --detach
```

## As a two step process
```bash
docker compose build --progress tty
docker compose up
```

# Software Requirements

* Docker
* `git`
* `make`
* a web browser

## Software Versions

Because software is in Docker containers (for reproducibility), the versions of the Docker software you're using matter. The
software in this repo has been tested with
* `docker compose version` yields "2.34.0-desktop.1" on a Mac Airbook arm64; "v2.2.1" on a Mac Airbook amd64
* Compose file format 3.6; see <https://docs.docker.com/reference/compose-file/>
* `docker --version` yields "Docker version 28.0.4, build b8034c0" on a Mac Airbook arm64; "Docker version 20.10.11" on a Mac Airbook amd64
See <https://docs.docker.com/compose/compose-file/compose-versioning/> for compatibility of versions.


## Troubleshooting and development

`docker-compose` instructions are from from
<https://github.com/ChloeCodesThings/chloe_flask_docker_demo>
and
<https://codefresh.io/docker-tutorial/hello-whale-getting-started-docker-flask/>

combining flask, gunicorn, nginx is from
<https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/>

nginx timeout
<https://wiki.ssdt-ohio.org/display/rtd/Adjusting+nginx-proxy+Timeout+Configuration>

# Licensing

Unless otherwise noted, all source code is covered by the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)


# Contributing

See CONTRIBUTING.md for guidance.

#EOF