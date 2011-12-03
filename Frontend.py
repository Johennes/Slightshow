##############################################################################
## Frontend.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

class Frontend(object):
    """Generic frontend class. Use this as a starting point to derive new
    frontends."""
    
    name = 'generic frontend'
    
    def __init__(self):
        """Constructor."""
        
        pass
    
    def supported_file_extensions(self):
        """Return a list of supported file extensions."""
        
        return []
