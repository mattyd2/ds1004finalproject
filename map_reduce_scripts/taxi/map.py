#!/usr/bin/python

import sys

for line in sys.stdin:
    l = line.strip().split(',')
    if l[0] != 'vendor_id':
        key = ','.join(l[0:3] + [l[5]])
        # start_time = l[1].split(' ')[1]
        # end_time = l[2].split(' ')[1]

        start_datetime = datetime.strptime(l[1], '%Y %M %D %X')
        end_datetime = datetime.strptime(l[2], '%b %d %Y %I:%M%p')
        if start_time < end_time:
            duration = end_time - start_time
        else:
            duration = start_time - end_time
            date_object = datetime.strptime(, '%b %d %Y %I:%M%p')
        #           0           1        2        3          4            5        6         7        8          9
        value = l[5]+l[6]+','+l[1]+','+l[6]+','+l[5]+','+l[9]+l[10]+','+l[2]+','+l[10]+','+l[9]+','+l[17]+','+
        print "%s\t%s" % (key, value)
