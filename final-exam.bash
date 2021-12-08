#!/bin/bash
examNames=[middle-earth10 middle-earth15 middle-earth20 middle-earth25 middle-earth30]

for e in examNames; do
    ./hill-climb.py $e >> FRODO.txt
done