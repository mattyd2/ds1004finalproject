#!/usr/bin/python

import sys

for line in sys.stdin:
    l = line.strip().split(',')
    key = l[3]+','+l[7]
    value = l[4]+','+l[1]+','+l[5]+','+l[6]+','+l[8]+','+l[2]+','+l[9]+','+l[10]+','+l[0]+',,'
    print "%s\t%s" % (key, value)
