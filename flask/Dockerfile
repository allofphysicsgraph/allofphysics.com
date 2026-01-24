# Physics Derivation Graph
# Ben Payne, 2026
# https://creativecommons.org/licenses/by/4.0/
# Attribution 4.0 International (CC BY 4.0)

# https://docs.docker.com/build/building/best-practices/

# https://docs.docker.com/engine/reference/builder/#from
# https://github.com/phusion/baseimage-docker
# https://hub.docker.com/r/phusion/baseimage/tags
FROM phusion/baseimage:jammy-1.0.4
# Ubuntu is too big
#FROM ubuntu:latest

# force stdin, stdout and stderr to be totally unbuffered (eg. avoid delayed prints).
# avoid python printing issues in docker containers.
ENV PYTHONUNBUFFERED=1

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disk (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1

# https://docs.docker.com/engine/reference/builder/#run
RUN apt-get update && \
    apt-get install -y \
# text editing
               vim \
               python3 \
               python3-pip \
               python3-dev \
# documentation generation
               python3-sphinx \
               build-essential  \
# generate pictures of graphs using dot
               graphviz \
# generate pictures of expressions using latex
               dvipng \
#               git-core \
# npm for mathjax
               npm \
#               automake \
#               autoreconf \
# compile .tex to .dvi
               texlive \
    && rm -rf /var/lib/apt/lists/*

# https://docs.docker.com/engine/reference/builder/#copy
# requirements.txt contains a list of the Python packages needed for the PDG
COPY requirements.txt /tmp

# need to set WORKDIR before running npm, otherwise the error is "npm ERR! Tracker "idealTree" already exists"
WORKDIR /tmp

# https://www.npmjs.com/package/mathjax
RUN npm install mathjax@3
#RUN npm install mathjax

# convert DVI to SVG
# not necessary, and written in Python2. Conversion to Python3 using 2to3 failed :(
#RUN git clone https://github.com/WojciechMula/pydvi2svg.git
#RUN ln -sf /app/pydvi2svg/dvi2svg.py /usr/local/bin/
#RUN cat pydvi2svg/dvi2png.py | sed 's/#!\/usr\/bin\/python/\/usr\/bin\/python3/' > pydvi2svg/dvi2png.py
#RUN cat pydvi2svg/conv/binfile.py | sed 's/binfile(file/binfile(filename/' > pydvi2svg/conv/binfile.py
#RUN git clone https://github.com/fontforge/fontforge.git
#RUN git clone https://github.com/fontforge/libspiro.git
#RUN git clone https://github.com/fontforge/libuninameslist.git

# TODO - https://github.com/allofphysicsgraph/proofofconcept/issues/82
#RUN tlmgr init-usertree
#RUN apt-get install -y texlive-base
#RUN apt-get install -y wget xzdec
#RUN /usr/bin/tlmgr install braket

# https://stackoverflow.com/a/63457606/1164295
RUN pip3 install --upgrade pip

RUN pip3 install -r /tmp/requirements.txt --no-cache-dir -vvv --ignore-installed blinker

RUN useradd --create-home appuser
WORKDIR       /home/appuser/app

RUN mkdir -p  /home/appuser/app/uploads
RUN mkdir -p  /home/appuser/app/tmp

COPY --chown=appuser:appuser templates     /home/appuser/app/templates
COPY --chown=appuser:appuser static        /home/appuser/app/static
RUN mv /tmp/node_modules/mathjax/es5 /home/appuser/app/static/mathjax

RUN chown -R appuser /home/appuser/app && chgrp -R appuser /home/appuser/app

USER appuser

COPY --chown=appuser:appuser \
     common_lib.py \
     compute.py \
     config.py \
     controller.py \
     latex_to_sympy.py \
     logs_to_stats.py \
     json_schema.py \
     Makefile \
     pdg_api.py \
     schema.sql \
     sql_db.py \
     user.py \
     validate_dimensions_sympy.py \
     validate_steps_sympy.py \
     cert.pem \
     key.pem \
     /home/appuser/app/

RUN echo "alias python=python3" > /home/appuser/.bashrc
RUN bash -l /home/appuser/.bashrc

# An ENTRYPOINT allows you to configure a container that will run as an executable.
ENTRYPOINT ["python3"]

# There can only be one CMD instruction in a Dockerfile
# The CMD instruction should be used to run the software contained by your image, along with any arguments.
CMD ["/home/appuser/app/controller.py"]


#EOF
