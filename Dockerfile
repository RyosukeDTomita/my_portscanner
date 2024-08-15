# Dev Container
#FROM python:3.12.4-bullseye AS devcontainer
FROM debian:bookworm-20240812 AS devcontainer

ARG PYTHON_VERSION=3.12.4

WORKDIR /app
COPY ../ .

# aqua install
RUN <<EOF
apt-get update -y
apt-get install -y --no-install-recommends wget ca-certificates
wget -q https://github.com/aquaproj/aqua/releases/download/v2.30.0/aqua_linux_amd64.tar.gz
rm -rf /usr/local/bin/aqua && tar -C /usr/local/bin/ -xzf aqua_linux_amd64.tar.gz
rm aqua_linux_amd64.tar.gz
EOF

# install packages and some tools.
# NOTE: rye is installed by aqua.
RUN <<EOF
aqua install
EOF

RUN <<EOF
PATH=$PATH":$(aqua root-dir)/bin"
rye pin ${PYTHON_VERSION}
rye sync
EOF

#pip install --upgrade pip setuptools wheel --no-cache-dir
# pip install -r requirements.lock --no-cache-dir



# # Build
# FROM debian:12.6-slim AS build

# LABEL version="0.0.0" \
#       author="RyosukeDTomita" \
#       docker_build="docker buildx bakey

# WORKDIR /opt/my_portscanner

# ARG USER_NAME="sigma"
# RUN <<EOF
# echo 'Creating `$USER_NAME` group.'
# addgroup {USER_NAME}
# echo 'Creating `$USER_NAME` user.'
# adduser -G ${USER_NAME} -g "my_portscanner user" -s /bin/bash -HD ${USER_NAME}
# EOF

# ENV PATH=${PATH}:/opt/my_portscanner

# USER ${USER_NAME}
# COPY --chown=sigma:sigma ["my_portscanner/", "/opt/nikto"]
# ENTRYPOINT ["/app/test.py"]
