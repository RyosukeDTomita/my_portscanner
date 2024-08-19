# MY PORT SCANNER like nmap

![un license](https://img.shields.io/github/license/RyosukeDTomita/my_portscanner)
[![pytest](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/pytest.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/pytest.yaml)
[![latest release](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/release.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/release.yaml)


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
docker run my_portscanner 192.168.150.35 -p 22,80,443,3306,5432
Starting my_portscanner 0.1.0 ( https://github.com/RyosukeDTomita/my_portscanner ) at 2024-08-18 20:06 JST
my_portscanner scan report for 192.168.150.35 (192.168.150.35)
connect scan
PORT       STATE SERVICE
22/tcp     open  unknown
```

- HELP

```shell
docker run my_portscanner -h
usage: my_portscanner [-h] [-sT] [-sS] [-oN FILE_TXT] [-p PORT] [--version]
                      target_ip

positional arguments:
  target_ip             set target ip address.

options:
  -h, --help            show this help message and exit
  -sT, --connect_scan   TCP connect scan
  -sS, --stealth_scan   TCP SYN scan
  -oN FILE_TXT, --file_txt FILE_TXT
                        output txt file name.
  -p PORT, --port PORT  port number lists
  --version             show program's version number and exit
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
