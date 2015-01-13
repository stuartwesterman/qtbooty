#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Mathew Cosgrove
# @Date:   2014-12-05 20:56:57
# @Last Modified by:   cosgroma
# @Last Modified time: 2015-01-12 21:29:27

import logging
logger = logging.getLogger(__name__)

import os
from os import path
import sys
# import logging
import json
from PyQt4 import QtCore, QtGui


class App(QtGui.QApplication):
  """
  @summary:
  """
  def __init__(self, json_file=None):
    """
    @summary:
    @param json_file:
    @result:
    """
    super(App, self).__init__(sys.argv)
    self.resources = path.join(path.dirname(__file__), 'resources')
    # Setup high level logging for this system
    # logging.basicConfig(format='%(asctime)s %(message)s',
    #                     datefmt='%m/%d/%Y %I:%M:%S %p')
    self.timers = []
    self.widgets = dict()
    self.app_settings = None

    # Process the app configuration file
    if json_file is not None and os.path.isfile(json_file):
      self.json_file = json_file
      self.app_settings = json.load(open(json_file))
    else:
      logger.critical('config file fucked up : %s' % (json_file))

    self.main = MainWindow(self.app_settings)
    self.apply_style("default")

  def add_widget(self, widget, params=None):
    self.main.layout.addWidget(widget)

  def add_timer(self, interval, callback):
    timer = QtCore.QTimer()
    timer.setInterval(interval)
    timer.timeout.connect(callback)
    self.timers.append(timer)

  def add_close_callback(self, callback):
    self.main.set_close_callback(callback)

  def apply_style(self, name):
    with open(path.join(self.resources, 'styles', 'style.css'), "r") as style:
      self.setStyleSheet(style.read())

  def update_status(self, message):
    self.main.update_status(message)

  def run(self):
    for timer in self.timers:
      timer.start()
    self.main.show()
    sys.exit(self.exec_())


class MainWindow(QtGui.QMainWindow):
  def __init__(self, settings=None):
    super(MainWindow, self).__init__()
    self.settings = settings
    self.menus = None
    self.layout = None
    self.close_callback = None

    # Setup the minimum structure before you process settings
    self.central = QtGui.QWidget()
    self.setCentralWidget(self.central)
    self.layout = QtGui.QVBoxLayout()
    self.central.setLayout(self.layout)

    # Process user settings
    if self.settings is not None:
      self.apply_settings()

  def apply_settings(self):
    self.central_setup()
    self.menu_setup()

  def central_setup(self):
    self.setWindowTitle(self.settings["name"])
    if self.settings["size"]["policy"] == "bounded":
      self.setMinimumSize(self.settings["size"]["min"][0],
                          self.settings["size"]["min"][1])
      self.resize(self.settings["size"]["max"][0],
                  self.settings["size"]["max"][1])

  def menu_setup(self):
    if self.settings["menu"]["enabled"]:
      self.menus = dict()
      for item in self.settings["menu"]["items"]:
        self.menus[item["name"]] = self.menuBar().addMenu(item["name"])
        self.menus[item["name"]].actions = dict()
        for action in item["actions"]:
          act = QtGui.QAction(action["name"], self,
                              shortcut=action["shortcut"],
                              statusTip=action["tip"])
          self.menus[item["name"]].actions[action["name"]] = act
          self.menus[item["name"]].addAction(self.menus[item["name"]].actions[action["name"]])

  def closeEvent(self, event):
    if self.close_callback is not None:
      self.close_callback()

  def update_status(self):
    if self.settings["status"]["enabled"]:
      self.statusBar().showMessage("")
    # also by default added the CPU percentage and memory usage

  def set_close_callback(self, callback):
    self.close_callback = callback


def close_test():
  print("Closed")

if __name__ == '__main__':
  app = App('tests/config/app_config.json')
  # app.add_close_callback(close_test)
  # app.main.menus["File"].actions["New"].triggered.connect(test_trigger)
  app.run()
  print("test", )
