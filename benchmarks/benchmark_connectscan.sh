#!/bin/bash
time docker run my_portscanner -sT -p- 192.168.150.58 --max-rtt-timeout 200 -d >> result.txt
for i in 8 16 32 64 128 256; do
  echo ----------max-parallelism $i----------
  time docker run my_portscanner -sT -p- 192.168.150.58 --max-rtt-timeout 200 --max-parallelism $i -d >> result.txt
  echo ----------end $i----------
done

