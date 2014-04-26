#!/usr/bin/python


import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    '''
    For every single unit, write a reducer that will return the busiest datetime (e.g.,
    the entry that had the most entries).  Ties should go to datetimes that are later on in the
    Month of May.  You can assume that the contents of the reducer will be sorted by UNIT, such that
    all entries corresponding to a given UNIT will be sorted together. The output should be the UNIT
    name, the datetime (which is a concatenation of date and time), and ridership separated by tabs.

    For example, the output of the reducer may look like this:
    R001    2011-05-11 17:00:00	   31213.0
    R002	2011-05-12 21:00:00	   4295.0
    R003	2011-05-05 12:00:00	   995.0
    R004	2011-05-12 12:00:00	   2318.0
    R005	2011-05-10 12:00:00	   2705.0
    R006	2011-05-25 12:00:00	   2784.0
    R007	2011-05-10 12:00:00	   1763.0
    R008	2011-05-12 12:00:00	   1724.0
    R009	2011-05-05 12:00:00	   1230.0
    R010	2011-05-09 18:00:00	   30916.0
    ...
    ...

    Since you are printing the actual output of your program, you
    can't print a debug statement without breaking the grader.
    Instead, you should use the logging module, which we've configured
    to log to a file which will be printed when you hit "Test Run".
    For example:
    logging.info("My debugging message")
    '''

    max_entries = 0
    old_key = None
    datetime = ''
    thisKey = ''
    # your code here
    for line in sys.stdin:
        data = line.split("\t")
        #logging.info(data[0] + " " + data[2] + " " + data[3])
        tKey = data[0]
        if old_key and old_key != tKey:
            val = '{0}\t{1}\t{2}'.format(old_key,datetime.strip(),max_entries)
            #logging.info(val)
            print val
            thisCount = data[1]
            max_entries = float(thisCount)
            datetime = '{0} {1}'.format(data[2],data[3])
        else:
            thisCount = float(data[1])
            if thisCount >= max_entries:
                max_entries = float(thisCount)
                datetime = '{0} {1}'.format(data[2],data[3])
             
        thisKey = tKey
        old_key = thisKey
        val = '{0}\t{1}\t{2}'.format(old_key,datetime.strip(),max_entries)
        print val
reducer()
#
