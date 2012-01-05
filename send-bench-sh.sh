#!/bin/bash

for i in "quad-i7-20-ssd" "dual-i7-27-ssd" "dual-i7-27-hd" "dual-i5-23-hd" ; do
    scp bench.sh $i.corp.sfo1.mozilla.com:bench.sh
done

