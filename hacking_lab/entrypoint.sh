#!/bin/bash
/etc/init.d/apache2 start & # backgroundで実行しないとsshdが起動できない。
/usr/sbin/sshd -D
