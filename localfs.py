from .api import fs
import os
import os.path
import stat
import datetime
import shutil

class FileInformation(fs.FileInformation):
	def __init__(self, path, parent):
		stats = os.stat(path)
		super(FileInformation, self).__init__(path, datetime.datetime.fromtimestamp(stats[stat.ST_CTIME]), stats[stat.ST_SIZE], parent)

	def download(self):
		return open(self.fullPath, 'rb')

	def upload(self, file):
		with open(self.fullPath, 'wb') as ofile:
			shutil.copyfileobj(file, ofile)

	def delete(self):
		os.remove(self.fullPath)


class DirectoryInformation(fs.DirectoryInformation):
	def __init__(self, path, parent = None):
		stats = os.stat(path)
		super(DirectoryInformation, self).__init__(path, datetime.datetime.fromtimestamp(stats[stat.ST_CTIME]), stats[stat.ST_SIZE], parent)

	def getFiles(self):
		for fn in os.listdir(unicode(self.fullPath)):
			fnFull = os.path.join(self.fullPath, fn)
			if os.path.isfile(fnFull):
				yield FileInformation(fnFull, self)

	def getDirectories(self):
		for fn in os.listdir(unicode(self.fullPath)):
			fnFull = os.path.join(self.fullPath, fn)
			if os.path.isdir(fnFull):
				yield DirectoryInformation(fnFull, self)

	def delete(self):
		os.remove(self.fullPath)

	def createDirectory(self, name):
		os.mkdir(os.path.join(self.fullPath,name))
		return DirectoryInformation(os.path.join(self.fullPath, name), self)

	def createFile(self, name, file):
		fnFull = os.path.join(self.fullPath, name)
		shutil.copyfileobj(file, open(fnFull, 'wb'))
		return FileInformation(fnFull, self)


class FileSystem(fs.FileSystem):
	rootDir = None
	def __init__(self, rootDir):
		self.rootDir = rootDir

	def getRoot(self):
		return DirectoryInformation(os.path.abspath(self.rootDir))