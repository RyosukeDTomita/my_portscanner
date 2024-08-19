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
rm -rf /var/lib/lists
EOF

# install packages and some tools.
# NOTE: rye is installed by aqua.
RUN <<EOF
aqua install
EOF

# build
RUN <<EOF
PATH=$PATH":$(aqua root-dir)/bin"
rye pin ${PYTHON_VERSION}
rye sync
rye build
EOF


FROM python:3.12.4-slim-bullseye AS run
ARG VERSION="0.1.2"

LABEL version="${VERSION}" \
      author="RyosukeDTomita" \
      docker_compose_build="docker buildx bake" \
      docker_build="docker buildx build . -t my_portscanner" \
      docker_compose_run="docker compose run my_portscanner_app localhost" \
      docker_run="docker run my_portscanner localhost"


WORKDIR /app

# create execution user with sudo
ARG USER_NAME="sigma"
RUN <<EOF
apt-get update -y
apt-get install -y --no-install-recommends sudo
echo 'Creating ${USER_NAME} group.'
addgroup ${USER_NAME}
echo 'Creating ${USER_NAME} user.'
adduser --ingroup ${USER_NAME} --gecos "my_portscanner user" --shell /bin/bash --no-create-home --disabled-password ${USER_NAME}
echo 'using sudo'
usermod -aG sudo ${USER_NAME}
echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
rm -rf /var/lib/lists
EOF

COPY --from=devcontainer --chown=${USER_NAME}:${USER_NAME} ["/app/dist/my_portscanner-${VERSION}-py3-none-any.whl", "/app/dist/my_portscanner-${VERSION}-py3-none-any.whl"]

# install app
RUN <<EOF
python3 -m pip install /app/dist/my_portscanner-${VERSION}-py3-none-any.whl
EOF

USER ${USER_NAME}

ENTRYPOINT ["sudo", "my_portscanner"]

