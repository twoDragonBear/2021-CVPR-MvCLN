#!/bin/bash
source /data2/chenyongcan/miniconda3/bin/activate MvCLN

for((i=1;i<=5;i++));  
do 
echo "Caltech101"
echo "-------------start---------------" 
python run.py --data 1 --gpu 4
echo "--------------end----------------"
done

