#!/bin/bash
cd /liveroute/miguroute
a=`lsof -i:1935 | wc -l`
if [ "$a" -gt "0" ];then
    echo "Booted"
else
	python3 /liveroute/miguroute/web_server.py 1935
	sleep 1
	/liveroute/miguroute/bootserver.sh $@
fi
