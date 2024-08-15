# MY PORT SCANNER like nmap

![un license](https://img.shields.io/github/license/RyosukeDTomita/my_portscanner)

## INDEX

- [ABOUT](#about)
- [LICENSE](#license)
- [ENVIRONMENT](#environment)
- [PREPARING](#preparing)
- [HOW TO USE](#how-to-use)

---

## ABOUT

Full scratch built [nmap](https://nmap.org/) respect port scanner.

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

## LICENSE

[unlicense](./LICENSE)

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

---

## HOW TO USE

```shell
# example
docker run -it my_portscanner localhost -p 22
```
