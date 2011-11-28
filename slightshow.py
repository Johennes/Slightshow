#!/usr/bin/python2

##############################################################################
## slightshow.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

import getopt, sys

def usage(error = None):
    if error:
        print 'Error:', error
    
    print 'USAGE: slightshow.py [OPTION...] FILE...'
    print ''
    print 'Options:'
    print '  -h, --help          Display this message and exit'
    print '  -r, --recursive     Recursively include directories'
    print '  -d, --delay MSECS   Delay between subsequent pictures in'
    print '                      milliseconds (default: 2000)'
    print '  -s, --shuffle       Display pictures in random order'
    print '  -l, --loop          Infinitely repeat the picture sequence'

def main():
    # Initialize default settings
    recursive = False
    delay = 2000
    shuffle = False
    loop = False
    
    # Parse CLI arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hrd:sl',
            ['help', 'recursive', 'delay=', 'shuffle', 'loop'])
    except getopt.GetoptError, err:
        usage(str(err))
        sys.exit(1)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-r', '--recursive'):
            recursive = True
        elif opt in ('-d', '--delay'):
            try:
                delay = int(arg)
            except ValueError, err:
                usage('non-numeric argument to option ' + opt)
                sys.exit(1)
        elif opt in ('-s', '--shuffle'):
            shuffle = True
        elif opt in ('-l', '--loop'):
            loop = True
        else:
            usage('unhandled option')
            sys.exit(1)

if __name__ == '__main__':
    main()