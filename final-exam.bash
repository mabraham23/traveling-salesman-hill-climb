#!/bin/bash

if [ -f FRODO.txt ]
then
  rm FRODO.txt
fi

# create a list of all files in the current directory
declare -a arr=("middle-earth10" "middle-earth15" "middle-earth20" "middle-earth25" "middle-earth30")

for i in "${arr[@]}"
do
  echo $i >> FRODO.txt
  ./hill-climb.py $i >> FRODO.txt
done