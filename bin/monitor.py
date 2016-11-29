#!/usr/bin/python
usage       = "monitor.py [--options] directory"
description = "a rather brute force way of monitoring the latency of files; should produce ~second level accuracy as long as --cadence<1.0. This seems to be necessary because the filesystem's timestamps are lying to me"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import sys
import os
import glob

import time
from lal.gpstime import tconvert

from optparse import OptionParser

#-------------------------------------------------

def getFiles( directory, mostRecent='', suffix='gwf', verbose=False ):

    ### glob filenames that are bigger than mostRecent
    globstring = '%s/*%s'%(directory, suffix)
    if verbose:
        print "glob : "+globstring

    filenames = sorted([filename for filename in glob.glob(globstring) if filename > mostRecent])

    if filenames: ### if there are any, update mostRecent
        mostRecent = filenames[-1]

    return filenames, mostRecent

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-v', '--verbose', default=False, action='store_true')
parser.add_option('-V', '--Verbose', default=False, action='store_true')

parser.add_option('-c', '--cadence', default=0.1, type='float',
    help='how often we query the filesystem' )

parser.add_option('-s', '--suffix', default='gwf', type='string',
    help='the suffix for the filename. DEFAULT="gwf"' )

opts, args = parser.parse_args()

if len(args)!=1:
    raise ValueError('please supply exactly 1 input argument\n%s'%usage)
directory = args[0]

opts.verbose = opts.verbose or opts.Verbose

#-------------------------------------------------

### deterimine initial state of directory
_, mostRecent = getFiles( directory, suffix=opts.suffix, verbose=opts.Verbose )
if opts.verbose:
    print >> sys.stdout, 'mostRecent : %s'%mostRecent

### iterate
while True:
    t0 = time.time() ### remember when we started

    ### discover new files
    filenames, mostRecent = getFiles( directory, mostRecent=mostRecent, suffix=opts.suffix, verbose=opts.Verbose) 

    ### print new files and their latencies
    gpsObs = tconvert('now') ### get the current gps time
    for filename in filenames:
        gpsNom = int(os.path.basename(filename).split('-')[-2]) ### get gps time from this filename

        ### report latency
        print >> sys.stderr, '%.1f\t%s'%(gpsObs-gpsNom, filename) 

    sys.stderr.flush()

    if opts.verbose:
        print >> sys.stdout, "mostRecent : %s at %.3f"%(mostRecent, gpsObs)

    ### sleep so we don't query faster than opts.cadence
    wait = max(0, t0+opts.cadence-time.time())
    if opts.verbose:
        print >> sys.stdout, "waiting %.3f seconds"%wait

    time.sleep( wait )
