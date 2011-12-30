#!/bin/bash

import csv
import sys
import StringIO
import itertools



def find_average_time(a,b):
    times=[]
    for i in range(0, len(a)):
        times.append(b[i] - a[i])
    return sum(times, 0.0) / len(times)

if len(sys.argv) != 2:
    exit(1)

# Strip trailing commas
data_file = open(sys.argv[1])
mem_data = StringIO.StringIO()
for line in data_file.readlines():
    print >> mem_data, line.strip().rstrip(',')
data_file.close()

mem_data.seek(0)

reader = csv.reader(mem_data)

headers = reader.next()
data = dict([(x,[]) for x in headers])
for row in reader:
    if len(row) == len(headers):
        for i in range(0,len(headers)):
            data[headers[i]].append(int(row[i]))


# Do stuff below here

print "Average end to end Time: ", find_average_time(data[headers[0]], data[headers[-1]])
for i in range(1,len(headers)):
    print 'Average time from %s to %s: %s' % (headers[i-1], headers[i], find_average_time(data[headers[i-1]], data[headers[i]]))
