#!/usr/bin/env python
# -*- coding: utf-8 -*-;
"""Name of module.

Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
  Examples can be given using either the ``Example`` or ``Examples``
  sections. Sections support any reStructuredText formatting, including
  literal blocks::

      $ python test_surf.py

Section breaks are created by simply resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
  module_level_variable (int): Module level variables may be documented in
    either the ``Attributes`` section of the module docstring, or in an
    inline docstring immediately following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

"""
# @Author: Mathew Cosgrove
# @Date:   2014-12-30 06:57:46
# @Last Modified by:   Mathew Cosgrove
# @Last Modified time: 2015-02-07 07:39:58
# REF: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html#example-google
# REF: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

__author__ = "Mathew Cosgrove"
__copyright__ = ""
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Mathew Cosgrove"
__email__ = "mathew.cosgrove@ngc.com"
__status__ = "Development"

import logging
import pyutils
pyutils.setup_logging()
logger = logging.getLogger()

import sys
from QtBooty import App
from QtBooty.graph import Surface, GraphScheduler
import numpy as np

app = App('../config/app_config.json')
surface = Surface()

gscheduler = GraphScheduler()
surf_updater = gscheduler.add_graph(surface, maxlen=10, interval=100, mode="array")
# np.histogram(nc_vals, bins=50, normed=True)

X = np.arange(0, 1023, 0.5)
Y = np.arange(-7000, 7000, 1000)
Z = np.arange(0, 10e6, 1e6)

# X = np.arange(-5, 5, 1)
# Y = np.arange(-5, 5, 1)
# Z = np.arange(0, 10, 1)

xlim = (np.min(X), np.max(X))
ylim = (np.min(Y), np.max(Y))
zlim = (np.min(Z), np.max(Z))

surface.set_xymesh(X, Y)
surface.set_lims(xlim, ylim, zlim)

# surface.set_boundary(X, Y, Z)
X, Y = np.meshgrid(X, Y)

def update():
  surf_updater.add_data(np.abs(np.random.normal(0, Z.ptp()/10.0, size=X.shape)), update.config)

update_surface_interval = 40

update.config = {
  "plots":[{
    "name": "cosine",
    "plot kwargs": {
      "pen": 'r',
      "downsample": None,
      "fillLevel": 0,
      "brush": (0, 0, 255, 80)
    }
  },{
    "name": "sine",
    "plot kwargs": {
      "pen": 'b',
      "downsample": None
    }
  }]
}

app.add_widget(surface)
app.add_timer(update_surface_interval, update)
# surface.set_interval(update_surface_interval*2)
gscheduler.start()
app.run()