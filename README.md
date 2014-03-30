Slightshow
==========

A command-line controlled tool for running randomized picture slideshows

This is a Python application that takes a bunch of images and displays them in
a fullscreen slideshow. The image paths as well as various configuration options
can be specified on the command line. Currently the frontend user interface
relies on PyGTK but the application is written in a modular way so that other
UI toolkits can easily be integrated.

### Usage

``` shell
slightshow [OPTION...] FILE...

Options:
  -h, --help            Display this message and exit
  -r, --recursive       Recursively include directories (default: disabled)
  -d, --delay MSECS     Delay between subsequent pictures in milliseconds
                        (default: 2000)
  -s, --shuffle         Display pictures in random order (default: disabled)
  -l, --loop            Infinitely repeat the picture sequence
                        (default: disabled)
  -f, --frontend NAME   Use the specified graphical frontend (default: gtk)
                        Available frontends: gtk
  -q, --quality N       Image scaling quality level (N=0..3, default: 2)
```
