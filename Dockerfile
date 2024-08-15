# Dev Container
#FROM python:3.12.4-bullseye AS devcontainer
FROM debian:bookworm-20240812 AS devcontainer

ARG PYTHON_VERSION=3.12.4
SHELL ["/bin/bash", "-c"]

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

# build
RUN <<EOF
PATH=$PATH":$(aqua root-dir)/bin"
rye pin ${PYTHON_VERSION}
rye sync
rye build
#VERSION=$(grep -m 1 '^version =' "pyproject.toml" | sed -E 's/version = "(.*)"/\1/')
#/app/.venv/bin/pip install dist/my_portscanner-${VERSION}.tar.gz
#/app/.venv/bin/pip install --target /app/dist dist/my_portscanner-0.1.0-py3-none-any.whl
EOF


FROM python:3.12.4-bullseye AS run

LABEL version="0.1.0" \
      author="RyosukeDTomita" \
      docker_build="docker buildx bakey"

WORKDIR /app

#ARG USER_NAME="sigma"
ARG USER_NAME="root"
# RUN <<EOF
# echo 'Creating ${USER_NAME} group.'
# addgroup ${USER_NAME}
# echo 'Creating ${USER_NAME} user.'
# adduser --ingroup ${USER_NAME} --gecos "my_portscanner user" --shell /bin/bash --no-create-home --disabled-password ${USER_NAME}
# EOF


ENV PATH=${PATH}:/app/.venv/bin

COPY --from=devcontainer --chown=${USER_NAME}:${USER_NAME} ["/app/dist", "/app/dist"]
COPY --from=devcontainer --chown=${USER_NAME}:${USER_NAME} ["/app/.venv", "/app/.venv"]
COPY --from=devcontainer --chown=${USER_NAME}:${USER_NAME} ["/root/.rye/py/cpython@3.12.4/bin/python3.12", "/root/.rye/py/cpython@3.12.4/bin/python3.12"]
 /root/.rye/py/cpython@3.12.4/bin/../lib/libpython3.12.so.1.0

RUN <<EOF
chmod +x /app/.venv/bin/python3
chmod +x /app/.venv/bin/my_portscanner
EOF

#USER ${USER_NAME}

# ENTRYPOINT ["/app/test.py"]
CMD ["my_portscanner", "--help"]
