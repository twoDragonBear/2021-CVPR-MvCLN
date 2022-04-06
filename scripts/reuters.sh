#!/bin/bash
source /data2/chenyongcan/miniconda3/bin/activate MvCLN

for((i=1;i<=5;i++));  
do
echo "Reuters_dim10"
echo "-------------start---------------"  
python run.py --data 2 --gpu 1
echo "--------------end----------------"
done

