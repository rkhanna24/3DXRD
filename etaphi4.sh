#!/bin/bash  

set -m

python etaphi.py 9 &
python etaphi.py 10 &
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done