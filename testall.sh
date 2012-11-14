#!/bin/bash

PATH1="malice_examples/archaeology/"
PATH2="malice_examples/valid/"
EXE="./compile"
OK1="output1.txt"
OK2="output2.txt"
CNT=0
MAX=$1

if [ -z $MAX ] ;
then
    MAX=1000
fi

for file in $PATH1*.alice 
do
    if [ $CNT -ge $MAX ] ;
    then 
        continue
    fi

    $EXE $file
    diff $OK1 $OK2
    CNT=$(expr $CNT + 1) 
done

for file in $PATH2*.alice
do
    if [ $CNT -ge $MAX ] ;
    then
        continue
    fi

    $EXE $file
    diff $OK1 $OK2
    CNT=$(expr $CNT + 1)
done

# ls $PATH1 | grep .alice | xargs -n1 -i $EXE $PATH1/{}
# ls $PATH2 | grep .alice | xargs -n1 -i $EXE $PATH2/{}

