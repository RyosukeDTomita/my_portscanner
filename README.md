# MY PORT SCANNER like nmap

![un license](https://img.shields.io/github/license/RyosukeDTomita/my_portscanner)
[![pytest](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/pytest.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/pytest.yaml)
[![latest release](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/release.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/release.yaml)
[![GitHub Container Registry](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/packages.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/packages.yaml)

## INDEX

- [ABOUT](#about)
- [ENVIRONMENT](#environment)
- [PREPARING](#preparing)
- [INSTALL](#install)
- [HOW TO USE](#how-to-use)
- [DEVELOPER MEMO](#developer-memo)

---

## ABOUT

Full scratch built [nmap](https://nmap.org/) respect port scanner.
- EXAMPLE

```shell
# Connect Scan
docker run my_portscanner -p 23-445 192.168.150.58 --max-rtt-timeout 200
Starting my_portscanner 0.1.3 ( https://github.com/RyosukeDTomita/my_portscanner ) at 2024-08-26 11:40 JST
my_portscanner scan report for 192.168.150.58 (192.168.150.58)
PORT       STATE    SERVICE
80/tcp     closed   unknown
443/tcp    closed   unknown

# SYN Scan
docker run my_portscanner -sS -p 22,80,443,8080 192.168.150.58 --max-rtt-timeout 200
Starting my_portscanner 0.1.3 ( https://github.com/RyosukeDTomita/my_portscanner ) at 2024-08-26 11:40 JST
my_portscanner scan report for 192.168.150.58 (192.168.150.58)
PORT       STATE    SERVICE
22/tcp     filtered unknown
80/tcp     closed   unknown
443/tcp    closed   unknown
8080/tcp   closed   unknown
```

- HELP

```shell
docker run my_portscanner -h
usage: my_portscanner [-h] [-sT] [-sS] [-p PORT]
                      [--max-rtt-timeout MAX_RTT_TIMEOUT] [--version]
                      [--max-parallelism MAX_PARALLELISM] [-d]
                      target_ip

positional arguments:
  target_ip             set target IP address or FQDN.

options:
  -h, --help            show this help message and exit
  -sT, --connect_scan   TCP connect scan (default)
  -sS, --stealth_scan   TCP SYN scan
  -p PORT, --port PORT  port number, port number lists, port number range.
                        e.g: -p 22 -p 22,80,443 -p 22-30 -p- (all port)
  --max-rtt-timeout MAX_RTT_TIMEOUT
                        set max rtt timeout (ms). default=1000
  --version             display my_portscanner version and exit
  --max-parallelism MAX_PARALLELISM
                        set max parallelism
  -d, --debug           display debug info
```

---

## ENVIRONMENT

- python 3.12.4

---

## INSTALL

### pulling from GitHub Container Registry

```shell
docker pull ghcr.io/ryosukedtomita/my_portscanner:latest
docker tag ghcr.io/ryosukedtomita/my_portscanner my_portscanner
docker image ls
REPOSITORY                              TAG       IMAGE ID       CREATED          SIZE
my_portscanner                          latest    59ed4a2aff25   15 minutes ago   195MB
ghcr.io/ryosukedtomita/my_portscanner   latest    59ed4a2aff25   15 minutes ago   195MB
```

### install from Releases

```shell
wget https://github.com/RyosukeDTomita/my_portscanner/releases/download/0.1.1/default.dist.my_portscanner-0.1.1-py3-none-any.whl
pip install ./default.dist.my_portscanner-0.1.1-py3-none-any.whl
```

### Local install

1. clone this repository
2. docker build

```shell
git clone https://github.com:RYosukeDTomita/my_portscanner.git
docekr buildx build -t my_portscanner .
```
> [!NOTE]
> if you want to use docker compose, please try this.
> ```shell
> docker buildx bake
> ```

---

## HOW TO USE

### running Docker

```shell
# example
docker run -it my_portscanner <FQDN or IP>
```

> [!NOTE]
> if you want to use docker compose, please try this.
> ```shell
> docker compose run my_portscanner_app localhost
> ```

### running on local

```shell
my_portscanner <FQDN or IP>
sudo my_portscanner <FQDN or IP > -sS
```

---

## DEVELOPER MEMO

### before creating version tag

Update version info
- Dockerfile
- src/my_portscanner/version.py
- ./pyproject.toml
