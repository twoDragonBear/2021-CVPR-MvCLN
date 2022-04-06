#!/bin/bash
source /data2/chenyongcan/miniconda3/bin/activate MvCLN

for((i=1;i<=5;i++));  
do
echo "Scene15"
echo "-------------start---------------"   
python run.py --data 0 --gpu 1
echo "--------------end----------------"   
done

