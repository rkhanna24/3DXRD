#!/bin/bash  

set -m

python etaphi.py 6 &
python etaphi.py 7 &
python etaphi.py 8 &
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done