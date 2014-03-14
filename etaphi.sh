#!/bin/bash 

# make sure you run chmod +x ./etaphi.sh before running this script

# Adjust the line below according how you parallelize it
chmod +x etaphi1.sh etaphi2.sh etaphi3.sh etaphi4.sh
# timing it is not necessary and you could use this line instead:
# ./etaphi.sh & ./etaphi2.sh & ./etaphi3.sh & ./etaphi4.sh &
(time ./etaphi1.sh & ./etaphi2.sh & ./etaphi3.sh & ./etaphi4.sh &) &> results.txt