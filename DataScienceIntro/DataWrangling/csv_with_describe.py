#!/usr/bin/python

import pandas
import pprint
def add_full_name(path_to_csv, path_to_new_csv):
    df = pandas.read_csv(path_to_csv)
    #print df['nameFirst']
    #df['nameFull'] = df['nameFirst'] + " " + df['nameLast']
    print df.describe()
print "hi"

add_full_name("test.csv", "out.csv")
