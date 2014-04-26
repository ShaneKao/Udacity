#!/usr/bin/python

import sys
import string
import logging

from util import mapper_logfile
logging.basicConfig(filename=mapper_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def mapper():
    """
    The input to this mapper will be the final Subway-MTA dataset, the same as
    in the previous exercise.  You can check out the csv and its structure below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    For each line of input, the mapper output should
    1) return the UNIT as the key
    2) return the number of ENTRIESn_hourly as the value
    3) Separate the key and the value by a tab, for example:
       R002\t105105.0

    Since you are printing the actual output of your program, you
    can't print a debug statement without breaking the grader.
    Instead, you should use the logging module which we've configured
    for you.
    
    For example:
    logging.info("My debugging message")
    
    The logging module can be used to give you more control over your debugging
    or other messages than you can get by printing them.  In this exercise, print
    statements from your mapper will go to your reducer, and print statements
    from your reducer will be considered your final output.  By contrast, messages
    logged via the loggers we configured will be saved to two files, one
    for the mapper and one for the reducer.  If you hit "Test Run", then we
    will show the contents of those files once your program has finished running.
    The logging module also has other capabilities; see 
    https://docs.python.org/2/library/logging.html for more information.
    """
    sys.stdin.readline()

    for line in sys.stdin:
        data = line.strip().split(",")
        unit = data[1]
        hourly = data[6].lower()
        #tword =  tword.translate(string.maketrans("",""), string.punctuation)
        val = "{0}\t{1}".format(unit,hourly)
        print val
        #logging.info(val)


mapper()

