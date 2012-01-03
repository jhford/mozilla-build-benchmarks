#!/bin/bash
# Clean up a file for loading into another program

import csv
import sys
import StringIO

def process_file(filename):
    # Strip trailing commas
    data_file = open(filename)
    mem_data = StringIO.StringIO()
    for line in data_file.readlines():
        print >> mem_data, line.strip().rstrip(',')
    data_file.close()

    mem_data.seek(0)

    outputfile = open(filename.replace('.csv', '') + '-processed.csv', 'wb')
    reader = csv.reader(mem_data)

    headers = reader.next()
    print >> outputfile, ','.join([x.replace('start', '') for x in headers[:-1]])
    for row in reader:
        if len(row) == len(headers):
            for i in range(1,len(headers)):
                outputfile.write(str(int(row[i]) - int(row[i-1])))
                if i+1 == len(headers):
                    outputfile.write("\n")
                else:
                    outputfile.write(",")

if len(sys.argv) <= 1:
    exit(1)

for i in sys.argv[1:]:
    process_file(i)
