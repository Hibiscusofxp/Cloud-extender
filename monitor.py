#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Filesystem Watcher and Automatic Command executer
@author 赵迤晨
@copyright 赵迤晨 (Zhao Yichen) <interarticle@gmail.com>
@license MIT License
@version 0.1.2

@changelog
v0.1.2: Implemented "first-matched, only-one-executed" rule, and unified path seperators to "/"
v0.1.1: Fixed incorrect CWD value when watch.yaml is in the same directory as watch.py, when executing locally.

modified for use in cloudextender by author
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import socket
import re
from os import path
import os
import threading
import yaml
import glob
import argparse
import subprocess
import fnmatch

import requests

import pointiofs
import localfs
import sync

import config


def setTimeout(timesec, func):
	t = threading.Timer(timesec, func)
	t.start()
	return t

class Handler(FileSystemEventHandler):
	file_changes = None
	monitor = None

	def __init__(self, monitor):
		self.file_changes = monitor.file_changes
		self.monitor = monitor

	def on_any_event(self, event):
		if type(event).__name__ == 'FileModifiedEvent' or type(event).__name__ == 'FileCreatedEvent':
			self.file_changes[event.src_path] = True
		elif type(event).__name__ == 'FileMovedEvent':
			self.file_changes[event.src_path] = False
			self.file_changes[event.dest_path] = True
		elif type(event).__name__ == 'FileDeletedEvent':
			self.file_changes[event.src_path] = False
		self.monitor.synchronize()

class Monitor:

	authorization = None
	rootPath = None

	file_changes = {}
	handler_timer = None
	handlingChanges = False
	change_delay = 1.5

	sync = None

	def __init__(self, authorization, rootPath):
		rootPath = os.path.abspath(rootPath)
		self.authorization = authorization
		self.rootPath = rootPath

		data = requests.get('https://api.point.io/v2/accessrules/list.json', headers={"Authorization": authorization}).json()

		remoteFS = []

		for row in pointiofs.table2dict(data):
			remoteFS.append(pointiofs.FileSystem(row['SHAREID'], authorization, row['SITETYPEID'], 'CloudExtender'))

		localFS = localfs.FileSystem(rootPath)

		self.sync = sync.MultiSynchronizer(localFS, remoteFS)


	def handleFileChanges(self):
		self.handler_timer = None
		self.handlingChanges = True
		if config.AUTO_SYNC:
			self.handleFileChangesInternal()
		self.handlingChanges = False

	def handleFileChangesInternal(self):
		local_file_changes = dict(self.file_changes)
		self.file_changes.clear()
		delete_files = []
		for path, preserve in local_file_changes.iteritems():
			if not preserve:
				path = path[len(self.rootPath):]
				path = path.replace('\\', '/').strip('/')
				delete_files.append(path)
		self.sync.synchronize(delete_files)

	def synchronize(self, immediate = False):
		if self.handler_timer:
			self.handler_timer.cancel()
		if not self.handlingChanges:
			#Fail silently if currently handling changes
			self.handler_timer = setTimeout(self.change_delay if not immediate else 0, self.handleFileChanges)



	def start(self):
		self.observer = Observer()
		self.observer.schedule(Handler(self), self.rootPath,recursive=True)
		self.observer.start()

