##############################################################################
## GTKFrontend.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

from Frontend import Frontend
from Util import roundrobin
import pygtk, gtk

class GTKFrontend(Frontend):
    """GTK+ frontend."""
    
    name = 'gtk'
    
    def __init__(self):
        """Constructor."""
        
        pass
    
    def supported_file_extensions(self):
        """Return a list of supported file extensions."""
        
        extensions = [i['extensions'] for i in gtk.gdk.pixbuf_get_formats()]
        return list(roundrobin(*extensions))
