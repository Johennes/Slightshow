##############################################################################
## Frontend.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

class Frontend(object):
    """Generic frontend class. Use this as a starting point to derive new
    frontends."""
    
    name = 'generic frontend'
    
    def __init__(self, quality):
        """Constructor."""
        
        self.has_stopped = False
    
    def supported_file_extensions(self):
        """Return a list of supported file extensions."""
        
        return []
    
    def run(self):
        """Run the frontend's main loop, if any."""
        
        pass
    
    def stop(self):
        """Stop the frontend's main loop, if any."""
        
        pass
    
    def display(self, path):
        """Display the image located at the specified path. Return True on
        success and False otherwise."""
        
        return False
