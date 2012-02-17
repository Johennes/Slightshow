#!/usr/bin/python2

##############################################################################
## Slightshow.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

import getopt, os, sys
from random import randint
from threading import Thread
from time import sleep, time

from Util import roundrobin

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

Frontend errors: %s\
''' % ', '.join(frontend_errors)
            exit(1)
        
        # Initialize default settings
        self.settings = {
            'recursive': False,
            'delay': 2,
            'shuffle': False,
            'loop': False,
            'frontend': frontends[0],
            'quality': 2
        }
        
        # Parse CLI arguments
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hrd:slf:q:',
                ['help', 'recursive', 'delay=', 'shuffle', 'loop',
                 'frontend=', 'quality='])
        except getopt.GetoptError, err:
            self.print_usage(str(err))
            sys.exit(1)
        
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.print_usage()
                sys.exit(0)
            elif opt in ('-r', '--recursive'):
                self.settings['recursive'] = True
            elif opt in ('-d', '--delay'):
                try:
                    self.settings['delay'] = int(arg) / 1000.0
                except ValueError, err:
                    self.print_usage('Non-numeric argument to option %s.'
                        % opt)
                    sys.exit(1)
            elif opt in ('-s', '--shuffle'):
                self.settings['shuffle'] = True
            elif opt in ('-l', '--loop'):
                self.settings['loop'] = True
            elif opt in ('-f', '--frontend'):
                try:
                    idx = [f.name for f in frontends].index(arg)
                    self.settings['frontend'] = frontends[idx]
                except ValueError:
                    self.print_usage('No frontend named %s available.' % arg)
                    exit(1)
            elif opt in ('-q', '--quality'):
                quality = self.settings['quality']
                
                try:
                    quality = int(arg)
                    assert quality in range(0,4)
                except (ValueError, AssertionError), err:
                    self.print_usage('Non-numeric argument to option %s.'
                        % opt)
                    sys.exit(1)
                
                self.settings['quality'] = quality
            else:
                self.print_usage('Unhandled option.')
                sys.exit(1)
        
        # Check if file arguments were supplied
        if not args:
            self.print_usage('No file arguments supplied.')
            sys.exit(1)
        
        # Load frontend & supported file extensions
        self.frontend = self.settings['frontend'](self.settings['quality'])
        extensions = self.frontend.supported_file_extensions()
        
        # Build list of supported files from supplied arguments
        self.files = []
        args.reverse()
        
        while args:
            # Pop next item
            item = args.pop()
            
            # Handle directories
            if os.path.isdir(item):
                if self.settings['recursive']:
                    for dirpath, _, filenames in os.walk(item):
                        filenames.reverse()
                        for filename in filenames:
                            args.append(os.path.join(dirpath, filename))
                    continue
            
            # Handle files
            if os.path.isfile(item):
                _, ext = os.path.splitext(item)
                if ext[1:].lower() in extensions:
                    self.files.append(item)
        
        # Check if any of the supplied files are supported
        if not self.files:
            print '''\
Error: None of the supplied files seems to be supported by the selected
frontend (%s). If you specified directories in the argument list make sure to
use the -r switch in order to scan them recursively.\
''' % self.frontend.name
            sys.exit(1)
        
        # Start slightshow iteration in background thread
        slightshow_thread = Thread(target = self.do_slightshow)
        slightshow_thread.start()
        
        # Run frontend in main thread
        self.frontend.run()
        
        # Wait for slightshow thread to terminate
        slightshow_thread.join()
    
    def do_slightshow(self):
        """Iterate through the collection of specified images and directories
        and display every image supported by the selected frontend."""
        
        # Initialize index stack and current starting time
        stack = self.new_index_stack()
        start = 0
        
        # Loop over collection of files
        while stack and not self.frontend.has_stopped:
            while stack and not self.frontend.has_stopped:
                # Store starting time
                start = time()
                
                # Display next item
                if self.frontend.display(self.pop_next_item(stack)):
                    break
            
            # Sleep
            delay = self.settings['delay'] - (time() - start)
            if delay > 0:
                for i in range(0, int(delay / 0.05)):
                    if not self.frontend.has_stopped:
                        sleep(0.05)
                
                # Remaining time difference won't be noticeable as it lies
                # beneath 50ms.
        
        self.frontend.stop()
    
    def new_index_stack(self):
        """Return a new index stack."""
        
        return range(len(self.files))
    
    def pop_next_item(self, stack):
        """Pops the next item using the supplied index stack."""
        
        # Pop next item
        item = None
        if self.settings['shuffle']:
            item = self.files[stack.pop(randint(0, len(stack) - 1))]
        else:
            item = self.files[stack.pop(0)]
        
        # Reset stack if in loop mode
        if not stack and self.settings['loop']:
            stack = self.new_index_stack()
        
        return item
    
    def print_usage(self, error = None):
        """Print usage information to STDOUT and display an optional error
        message."""
        
        if error:
            print 'Error: %s' % error
        
        print '''\
USAGE: slightshow [OPTION...] FILE...

Options:
  -h, --help            Display this message and exit\
'''
        print '''\
  -r, --recursive       Recursively include directories (default: %s)\
''' % self.option_enabled_string('recursive')
        
        print '''\
  -d, --delay MSECS     Delay between subsequent pictures in milliseconds
                        (default: %s)\
''' % int(self.settings['delay'] * 1000)
        
        print '''\
  -s, --shuffle         Display pictures in random order (default: %s)\
''' % self.option_enabled_string('shuffle')
        
        print '''\
  -l, --loop            Infinitely repeat the picture sequence
                        (default: %s)\
''' % self.option_enabled_string('loop')
        
        print '''\
  -f, --frontend NAME   Use the specified graphical frontend (default: %s)
                        Available frontends: %s\
''' % (frontends[0].name, ', '.join([f.name for f in frontends]))
        
        print '''\
  -q, --quality N       Image scaling quality level (N=0..3, default: %s)\
''' % self.settings['quality']
    
    def option_enabled_string(self, option):
        """Return a string indicating whether the specified option is
        enabled or not."""
        
        if self.settings[option]:
            return 'enabled'
        else:
            return 'disabled'

if __name__ == '__main__':
    Slightshow()
