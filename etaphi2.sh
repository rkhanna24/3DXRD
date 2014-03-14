#!/bin/bash  

set -m

python etaphi.py 3 &
python etaphi.py 4 &
python etaphi.py 5 &
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done