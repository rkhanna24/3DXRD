#!/bin/bash  

set -m

python etaphi.py 0 &
python etaphi.py 1 &
python etaphi.py 2 &
python etaphi.py 3 &
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done