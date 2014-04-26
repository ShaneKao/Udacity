#!/usr/bin/python

import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    '''
    Given the output of the mapper for this exercise, the reducer should return
    one row per unit, along with the total number of ENTRIESn_hourly over the
    course of May (which is the duration of our data).

    You can assume that the input to the reducer is sorted by UNIT, such that all rows
    corresponding to a particular UNIT are grouped together.

    The output should have a unit (the key) follow by a tab, follow by a value.
    An example output row from the reducer might look like this:
    R001\t500625.0

    Since you are printing the actual output of your program, you
    can't print a debug statement without breaking the grader.
    Instead, you should use the logging module, which we've configured
    to log to a file which will be printed when you hit "Test Run".
    For example:
    logging.info("My debugging message")
    '''

    entries = 0
    old_key = None

    for line in sys.stdin:
        data = line.split("\t")
        val = "{0}\t{1}".format(data[0],data[1])
        thisKey = data[0]
        if thisKey != old_key and old_key:
            op = "{0}\t{1}".format(old_key,entries)
            logging.info(op)
            print op
            entries = float(data[1])
        else:
            entries = entries + float(data[1])
            
        old_key = thisKey     
        #logging.info(val.strip())
    
    lastone = "{0}\t{1}".format(old_key,entries)
    print lastone
reducer()

