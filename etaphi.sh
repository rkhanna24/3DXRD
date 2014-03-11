#!/bin/bash  

# run:
#		(time ./etaphi.sh) &> results.txt
set -m

echo "This script will convert all the files in the directory" 
echo "		indicated in etaphi.py to etaphi maps"
echo "Please make sure that the parameter file required by"
echo "		etaphi.py is already written by rings.py"
echo "--------------------------------------------------------"

python etaphi.py 0 &
python etaphi.py 1 &
python etaphi.py 2 &
python etaphi.py 3 &
python etaphi.py 4 &
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done
python etaphi.py 5 &
python etaphi.py 6 &
python etaphi.py 7 &
python etaphi.py 8 &
python etaphi.py 9 &
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done
python etaphi.py 10