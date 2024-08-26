## nmap

```shell
# Connect Scan
time sudo nmap -sT -p- --max-rtt-timeout 200ms 192.168.150.58
Starting Nmap 7.80 ( https://nmap.org ) at 2024-08-26 23:28 JST
Nmap scan report for x1carbon (192.168.150.58)
Host is up (0.000050s latency).
Not shown: 65530 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
902/tcp  open  iss-realsecure
1716/tcp open  xmsg
3128/tcp open  squid-http
8834/tcp open  nessus-xmlrpc

Nmap done: 1 IP address (1 host up) scanned in 1.67 seconds
sudo nmap -sT -p- --max-rtt-timeout 200ms 192.168.150.58  0.27s user 1.06s system 78% cpu 1.686 total

# SYN Scan
time sudo nmap -sS -p- --max-rtt-timeout 200ms 192.168.150.58
Starting Nmap 7.80 ( https://nmap.org ) at 2024-08-26 23:27 JST
Nmap scan report for x1carbon (192.168.150.58)
Host is up (0.0000030s latency).
Not shown: 65530 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
902/tcp  open  iss-realsecure
1716/tcp open  xmsg
3128/tcp open  squid-http
8834/tcp open  nessus-xmlrpc

Nmap done: 1 IP address (1 host up) scanned in 0.64 seconds
sudo nmap -sS -p- --max-rtt-timeout 200ms 192.168.150.58  0.31s user 0.85s system 177% cpu 0.653 total
```

---

## my_portscanner

### version 0.2.0 (SYN Scan is 10 times faster than version 0.1.3)

```shell
# Connect Scan
time docker run my_portscanner -p- -sT --max-rtt-timeout 200 192.168.150.58
Starting my_portscanner 0.2.0 ( https://github.com/RyosukeDTomita/my_portscanner ) at 2024-08-26 23:26 JST
my_portscanner scan report for 192.168.150.58 (192.168.150.58)
PORT       STATE    SERVICE
22/tcp     open     unknown
902/tcp    open     unknown
1716/tcp   open     unknown
3128/tcp   open     unknown
8834/tcp   open     unknown
docker run my_portscanner -p- -sT --max-rtt-timeout 200 192.168.150.58  0.03s user 0.02s system 0% cpu 6.437 total

# SYN Scan
time docker run my_portscanner -p- -sS --max-rtt-timeout 200 192.168.150.582
Starting my_portscanner 0.2.0 ( https://github.com/RyosukeDTomita/my_portscanner ) at 2024-08-26 22:55 JST
my_portscanner scan report for 192.168.150.58 (192.168.150.58)
PORT       STATE    SERVICE
2/tcp      filtered unknown
4/tcp      filtered unknown
6/tcp      filtered unknown
7/tcp      filtered unknown
8/tcp      filtered unknown
22/tcp     open     unknown
53/tcp     filtered unknown
88/tcp     filtered unknown
120/tcp    filtered unknown
902/tcp    open     unknown
1716/tcp   open     unknown
3128/tcp   open     unknown
8834/tcp   open     unknown
docker run my_portscanner -p- -sS --max-rtt-timeout 200 192.168.150.58  0.06s user 0.03s system 0% cpu 5:52.44 total
```

#### parallelism

- SYN Scan

```shell
for i in $(seq 1 8); do
  echo ----------max-parallelism $i----------
  time docker run my_portscanner -sS -p- 192.168.150.58 --max-rtt-timeout 200 --max-parallelism $i -d >> result.txt
  echo ----------end $i----------
done
----------max-parallelism 1----------

real	50m21.649s
user	0m0.209s
sys	0m0.052s
----------end 1----------
----------max-parallelism 2----------

real	28m13.303s
user	0m0.136s
sys	0m0.017s
----------end 2----------
----------max-parallelism 3----------

real	19m24.560s
user	0m0.108s
sys	0m0.016s
----------end 3----------
----------max-parallelism 4----------

real	15m8.235s
user	0m0.083s
sys	0m0.029s
----------end 4----------
----------max-parallelism 5----------

real	12m34.572s
user	0m0.043s
sys	0m0.050s
----------end 5----------
----------max-parallelism 6----------

real	10m53.250s
user	0m0.065s
sys	0m0.020s
----------end 6----------
----------max-parallelism 7----------

real	9m33.677s
user	0m0.058s
sys	0m0.021s
----------end 7----------
----------max-parallelism 8----------

real	8m34.884s
user	0m0.074s
sys	0m0.004s
----------end 8----------
```

```shell
for i in 8 16 32 64 128 256; do
  echo ----------max-parallelism $i----------
  time docker run my_portscanner -sS -p- 192.168.150.58 --max-rtt-timeout 200 --max-parallelism $i -d >> result.txt
  echo ----------end $i----------
done
----------max-parallelism 8----------

real	8m33.690s
user	0m0.050s
sys	0m0.030s
----------end 8----------
----------max-parallelism 16----------

real	5m53.233s
user	0m0.049s
sys	0m0.018s
----------end 16----------
----------max-parallelism 32----------

real	5m54.537s
user	0m0.056s
sys	0m0.007s
----------end 32----------
----------max-parallelism 64----------

real	5m54.923s
user	0m0.032s
sys	0m0.033s
----------end 64----------
----------max-parallelism 128----------

real	5m54.669s
user	0m0.051s
sys	0m0.013s
----------end 128----------
----------max-parallelism 256----------

real	5m55.208s
user	0m0.044s
sys	0m0.021s
----------end 256----------
```

- Connect Scan

```shell
time docker run my_portscanner -sT -p- 192.168.150.58 --max-rtt-timeout 200 -d >> result.txt
for i in 8 16 32 64 128 256; do
  echo ----------max-parallelism $i----------
  time docker run my_portscanner -sT -p- 192.168.150.58 --max-rtt-timeout 200 --max-parallelism $i -d >> result.txt
  echo ----------end $i----------
done

real	0m9.739s
user	0m0.045s
sys	0m0.022s
----------max-parallelism 8----------

real	0m10.291s
user	0m0.049s
sys	0m0.021s
----------end 8----------
----------max-parallelism 16----------

real	0m9.642s
user	0m0.052s
sys	0m0.011s
----------end 16----------
----------max-parallelism 32----------

real	0m8.424s
user	0m0.054s
sys	0m0.016s
----------end 32----------
----------max-parallelism 64----------

real	0m8.963s
user	0m0.052s
sys	0m0.013s
----------end 64----------
----------max-parallelism 128----------

real	0m9.058s
user	0m0.042s
sys	0m0.020s
----------end 128----------
----------max-parallelism 256----------

real	0m9.071s
user	0m0.052s
sys	0m0.015s
----------end 256---------
```

### version 0.1.3 (Before Asynchronous processing)

```shell
# Connect Scan
time docker run my_portscanner -p0-65535 -sT --max-rtt-timeout 200 192.168.150.582
22/tcp     open     unknown
902/tcp    open     unknown
1716/tcp   open     unknown
3128/tcp   open     unknown
8834/tcp   open     unknown
docker run ghcr.io/ryosukedtomita/my_portscanner:0.1.3 -sT -p0-65535  200   0.04s user 0.03s system 4% cpu 1.712 total

# Syn Scan
time docker run ghcr.io/ryosukedtomita/my_portscanner:0.1.3 -sS -p0-65535 --max-rtt-timeout 200 192.168.150.58
22/tcp     open     unknown
902/tcp    open     unknown
1716/tcp   open     unknown
3128/tcp   open     unknown
8834/tcp   open     unknown
docker run ghcr.io/ryosukedtomita/my_portscanner:0.1.3 -sS -p0-65535  200  >   0.17s user 0.09s system 0% cpu 52:05.27 total
```
