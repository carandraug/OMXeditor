#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools

import cairo
import rsvg

import OMXeditor

def svg2png (fin, fout):
  svg = rsvg.Handle(file = fin)
  surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                               svg.props.width, svg.props.height)
  svg.render_cairo(cairo.Context(surface))
  surface.write_to_png(fout)

icon_names = {
  "database-symbol.svg"         : "auto-align.png",
  "download-from-the-cloud.svg" : "export-parameters.png",
  "folded-map.svg"              : "project-resize.png",
  "play-round-button.svg"       : "batch-process.png",
  "settings-lines.svg"          : "view-controls.png",
  "share-symbol.svg"            : "split-merge.png",
  "upload-to-cloud.svg"         : "load-parameters.png",
}

for fin, fout in icon_names.items ():
  svg2png (os.path.join ("OMXeditor", "data", fin),
           os.path.join ("OMXeditor", "data", fout))

setuptools.setup (
  name      = "OMXeditor",
  version   = OMXeditor.__version__,
  packages  = setuptools.find_packages (),

  entry_points = {
    "console_scripts": [
      "editor = OMXeditor.editor:main",
    ],
    "gui_scripts": [
      "OMXeditor = OMXeditor:main",
    ],
  },

  install_requires = [
    "matplotlib",
    "numpy",
    "PyOpenGL",
    "scipy",
    "wxPython",
  ],

  package_data = {
    "OMXeditor" : [os.path.join ("data", f) for f in (icon_names.keys ()
                                                      + icon_names.values ())],
  },
)
