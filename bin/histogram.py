#!/usr/bin/python
usage       = "histogram.py [--options] monitor.err"
description = "takes a histogram of the times reported in monitor.err (monitor.py prints latencies to stderr). Can automatically update the histogram if desired"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import os
import time

import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from optparse import OptionParser

#-------------------------------------------------

def extract( file_obj ):
    dts = []
    line = file_obj.readline()
    while line:
        dts.append( float(line.strip().split()[0]) )
        line = file_obj.readline()
    return dts

def plot( dts ):
    fig = plt.figure()
    ax  = fig.gca()

    ax.hist( dts, bins=max(len(dts)**0.5, 10) )

    ax.set_xlabel('latency (sec)')
    ax.set_ylabel('count')

    return fig, ax

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-v', '--verbose', default=False, action='store_true')

parser.add_option('-c', '--cadence', default=0.1, type='float',
    help='the cadence at which we check monitor.err for updates. \
If --one-off is supplied, this is ignored.' )

parser.add_option('', '--one-off', default=False, action='store_true' )

parser.add_option('-o', '--output-dir', default='.', type='string')
parser.add_option('-t', '--tag', default='', type='string')

opts, args = parser.parse_args()

if len(args)!=1:
    raise ValueError('please supply exactly 1 input argument\n%s'%usage)
moniterr = args[0] ### THIS IS A GOOD PUN

if opts.tag:
    opts.tag = "_"+opts.tag

#-------------------------------------------------

### load in existing numbers
if opts.verbose:
    print( 'reading in data from : %s'%moniterr )
file_obj = open(moniterr, 'r')

dts = []
dts += extract( file_obj )

if dts:
    ### plot
    fig, ax = plot( dts )

    ### save
    figname = "%s/monitor%s.png"%(opts.output_dir, opts.tag)
    if opts.verbose:
        print('saving : '+figname)
    fig.savefig(figname)
    plt.close(fig)

#-------------------------------------------------

### periodically update
if not opts.one_off:
    mtime = os.path.getmtime( moniterr ) ### last modification time

    while True:
        t0 = time.time()

        ntime = os.path.getmtime( moniterr )
        if mtime != ntime:

            mtime = ntime
            new = extract( file_obj )
            dts += new

            if opts.verbose:
                print('%s updated -> %d new lines'%(moniterr, len(new)))

            ### plot
            fig, ax = plot( dts )

            ### save
            if opts.verbose:
                print('saving : '+figname)
            fig.savefig(figname)
            plt.close(fig)

        wait = max(0, t0+opts.cadence-time.time())
        if opts.verbose:
            print('sleeping %.3f seconds'%wait)
        time.sleep(wait)
