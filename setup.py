#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup (
  name      = "OMXeditor",
  version   = "2.6-dev",
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
)
