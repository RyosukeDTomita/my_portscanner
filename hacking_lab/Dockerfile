FROM debian:bookworm-20240812-slim
ARG VERSION="0.0.0"
LABEL version="${VERSION}" \
      author="RyosukeDTomita" \
      docker_compose_build="docker buildx bake" \
      docker_build="docker buildx build . -t hacking_lab" \
      docker_compose_run="docker compose run hacking_lab_app" \
      docker_run="docker run my_portscanner hakcking_lab"

# 環境変数の設定
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_USER=myuser
ENV MYSQL_PASSWORD=mypassword
ENV MYSQL_DATABASE=mydatabase

RUN <<EOF
  apt-get update -y
  apt-get install -y --no-install-recommends apache2 openssh-server
  rm -rf /var/lib/apt/lists/*
EOF

# ssh settings
RUN <<EOF
  mkdir /var/run/sshd
  echo "root:root" | chpasswd # id:password
  echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
  echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
  echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config
EOF

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22 80

CMD ["/entrypoint.sh"]
