#!/usr/bin/python2

##############################################################################
## Slightshow.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

import getopt, sys

# Try to import frontends
frontends = []
frontend_errors = []
try:
    from GTKFrontend import GTKFrontend
    frontends.append(GTKFrontend)
except ImportError as error:
    frontend_errors.append(str(error))

class Slightshow(object):
    """Slightshow application base class."""
    
    def __init__(self):
        """Constructor."""
        # Check frontend availability
        if not frontends:
            print '''\
Error: Couldn't load any frontends. Make sure the application's minimum
dependencies are installed correctly. Below is a list of the errors
encountered during frontend loading.

Frontend errors: %s''' % ', '.join(frontend_errors)
            exit(1)
        
        # Initialize default settings
        settings = {
            'recursive': False,
            'delay': 2000,
            'shuffle': False,
            'loop': False,
            'frontend': frontends[0]
        }
        
        # Parse CLI arguments
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hrd:slf:',
                ['help', 'recursive', 'delay=', 'shuffle', 'loop',
                 'frontend='])
        except getopt.GetoptError, err:
            self.print_usage(str(err))
            sys.exit(1)
        
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.print_usage()
                sys.exit(0)
            elif opt in ('-r', '--recursive'):
                settings['recursive'] = True
            elif opt in ('-d', '--delay'):
                try:
                    settings['delay'] = int(arg)
                except ValueError, err:
                    self.print_usage('Non-numeric argument to option %s.'
                        % opt)
                    sys.exit(1)
            elif opt in ('-s', '--shuffle'):
                settings['shuffle'] = True
            elif opt in ('-l', '--loop'):
                settings['loop'] = True
            elif opt in ('-f', '--frontend'):
                try:
                    idx = [f.name for f in frontends].index(arg)
                    settings['frontend'] = frontends[idx]
                except ValueError:
                    self.print_usage('No frontend named %s available.' % arg)
                    exit(1)
            else:
                self.print_usage('Unhandled option.')
                sys.exit(1)
        
        # Load frontend & supported file extensions
        frontend = settings['frontend']()
        extensions = frontend.supported_file_extensions()
    
    def print_usage(self, error = None):
        """Print usage information to STDOUT and display an optional error
        message."""
        
        if error:
            print 'Error: %s' % error
        
        print '''\
USAGE: slightshow [OPTION...] FILE...

Options:
  -h, --help            Display this message and exit
  -r, --recursive       Recursively include directories
  -d, --delay MSECS     Delay between subsequent pictures in milliseconds
                        (default: 2000)
  -s, --shuffle         Display pictures in random order
  -l, --loop            Infinitely repeat the picture sequence
  -f, --frontend NAME   Use the specified graphical frontend (default: %s)
                        Available frontends: %s''' \
            % (frontends[0].name, ', '.join([f.name for f in frontends]))

if __name__ == '__main__':
    Slightshow()
