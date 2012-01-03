#!/bin/bash

import csv
import sys
import StringIO
import math

def get_times(a,b):
    times=[]
    for i in range(0, len(a)):
        times.append(b[i] - a[i])
    return times

def find_average_time(a,b):
    times=get_times(a,b)
    return sum(times, 0.0) / len(times)

def find_stddev(a,b):
    times = get_times(a,b)
    mean = find_average_time(a,b)
    deviations = 0
    for i in times:
        deviation = i - mean
        deviations += deviation * deviation
    return math.sqrt(deviations / (len(times) - 1))

def find_average_from_file(filename):
    # Strip trailing commas
    data_file = open(filename)
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

    return headers, data

if len(sys.argv) != 2:
    exit(1)

headers, data = find_average_from_file(sys.argv[1])

print "Average end to end Time: %s, stddev: %s" % (find_average_time(data[headers[0]], data[headers[-1]]), find_stddev(data[headers[0]], data[headers[-1]]))
for i in range(1,len(headers)):
    print 'Average time from %s to %s: %s, stddev: %s' % (headers[i-1], headers[i], find_average_time(data[headers[i-1]], data[headers[i]]), find_stddev(data[headers[i-1]], data[headers[i]]))
