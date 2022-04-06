#!/bin/bash
source /data2/chenyongcan/miniconda3/bin/activate MvCLN

for((i=1;i<=5;i++));  
do
echo "NoisyMNIST"
echo "-------------start---------------"  
python run.py --data 3 --gpu 3
echo "--------------end----------------"
done

