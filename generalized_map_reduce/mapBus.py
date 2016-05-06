#!/usr/bin/python

# http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-plan-input-distributed-cache.html
# mappings -- https://docs.google.com/spreadsheets/d/1kBPt5aOic7KlyvVIHv7dhrKH7DFZJRNzEC4DvfWr04A/edit?usp=sharing

import sys

for line in sys.stdin:
    l = line.strip().split(',')
    key = l[0]
    value = l[1]
    print "%s\t%s" % (key, value)
