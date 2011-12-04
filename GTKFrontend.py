##############################################################################
## GTKFrontend.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

from Frontend import Frontend
from Util import roundrobin
import pygtk, gtk, gobject

gobject.threads_init()

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
    
    def run(self):
        """Run the frontend's main loop."""
        
        gtk.main()
    
    def stop(self):
        """Stop the frontend's main loop."""
        
        gobject.idle_add(gtk.main_quit)
