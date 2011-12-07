##############################################################################
## GTKFrontend.py
##
## Copyright 2011 Johannes Marbach. All rights reserved.
## See the LICENSE file for details.

import sys
import pygtk, gtk, gobject

from Frontend import Frontend
from Util import roundrobin

gobject.threads_init()

class GTKFrontend(Frontend):
    """GTK+ frontend."""
    
    name = 'gtk'
    
    def __init__(self, quality):
        """Constructor."""
        
        # Query quality constant
        if quality == 0:
            self.quality = gtk.gdk.INTERP_NEAREST
        elif quality == 1:
            self.quality = gtk.gdk.INTERP_TILES
        elif quality == 2:
            self.quality = gtk.gdk.INTERP_BILINEAR
        elif quality == 3:
            self.quality = gtk.gdk.INTERP_HYPER
        
        # Initialize window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        # Initialize image widget
        self.image = gtk.Image()
        self.window.add(self.image)
        
        # Show window
        self.window.fullscreen()
        self.window.show_all()
    
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
    
    def display(self, path):
        """Display the image located at the specified path. Return True on
        success and False otherwise."""
        
        try:
            # Load image into pixbuf
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
            
            # Scale image
            p_width = pixbuf.get_width()
            p_height = pixbuf.get_height()
            w_width, w_height = self.window.get_size()
            
            width = 0
            height = 0
            
            if float(p_width) / float(p_height) > \
               float(w_width) / float(w_height):
                if p_width > w_width:
                    width = w_width
                    height = int(float(w_width) / float(p_width)
                        * float(p_height))
            else:
                if p_height > w_height:
                    width = int(float(w_height) / float(p_height)
                        * float(p_width))
                    height = w_height
            
            pixbuf = pixbuf.scale_simple(width, height, self.quality)
            
            # Display image
            gobject.idle_add(self.image.set_from_pixbuf, pixbuf)
            
            return True
        except:
            return False
