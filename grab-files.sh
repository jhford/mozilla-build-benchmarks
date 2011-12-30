#!/bin/bash

mkdir "$1"

for i in "quad-i7-20-ssd" "dual-i7-27-ssd" "dual-i7-27-hd" "dual-i5-23-hd" ; do
    scp $i.corp.sfo1.mozilla.com:bench-data.csv "$1"/$i-bench-data.csv
done

