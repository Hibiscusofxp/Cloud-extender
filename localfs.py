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


class FileSystem(fs.FileSystem):
	rootDir = None
	def __init__(self, rootDir):
		self.rootDir = rootDir

	def getRoot(self):
		return DirectoryInfo(os.path.abspath(rootDir))