#!/usr/bin/python
usage       = "histogram.py [--options] monitor.err"
description = "takes a histogram of the times reported in monitor.err (monitor.py prints latencies to stderr). Can automatically update the histogram if desired"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import os

import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-v', '--verbose', default=False, action='store_true')

parser.add_option('-c', '--cadence', default=0.1, type='float',
    help='the cadence at which we check monitor.err for updates. \
If --one-off is supplied, this is ignored.' )

parser.add_option('', '--one-off', default=False, action='store_true' )

opts, args = parser.parse_args()

if len(args)!=1:
    raise ValueError('please supply exactly 1 input argument\n%s'%usage)
moniterr = args[0] ### THIS IS A GOOD PUN

#-------------------------------------------------

### load in existing numbers
if opts.verbose:
    print( 'reading in data from : %s'%moniterr )
file_obj = open(moniterr, 'r')

for line in file_obj:
    raise NotImplementedError('WRITE ME')
