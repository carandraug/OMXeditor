#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

import OMXeditor

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
)
