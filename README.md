# MY PORT SCANNER like nmap

![un license](https://img.shields.io/github/license/RyosukeDTomita/my_portscanner)
[![pytest](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/pytest.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/pytest.yaml)
[![latest release](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/release.yaml/badge.svg)](https://github.com/RyosukeDTomita/my_portscanner/actions/workflows/release.yaml)


## INDEX

- [ABOUT](#about)
- [ENVIRONMENT](#environment)
- [PREPARING](#preparing)
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
usage: my_portscanner [-h] [-sT CONNECT_SCAN] [-oN FILE_TXT] [-p PORT] [-v]
                      target_ip

positional arguments:
  target_ip             set target ip address.

options:
  -h, --help            show this help message and exit
  -sT CONNECT_SCAN, --connect_scan CONNECT_SCAN
                        TCP connect Scan
  -oN FILE_TXT, --file_txt FILE_TXT
                        output txt file name.
  -p PORT, --port PORT  port number lists
  -v, --version         show program's version number and exit
```

---

## ENVIRONMENT

- python 3.12.4

---

## PREPARING

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

```shell
# example
docker run -it my_portscanner localhost -p 22
```

> [!NOTE]
> if you want to use docker compose, please try this.
> ```shell
> docker compose run my_portscanner_app localhost
> ```

---

## DEVELOPER MEMO

### before creating version tag

Update version info
- Dockerfile
- src/my_portscanner/version.py
- ./pyproject.toml
