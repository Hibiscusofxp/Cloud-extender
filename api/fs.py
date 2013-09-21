"""
API Interface Definition for FileSystem Access
"""

import dateutil.parser
import os.path

class FileSystemError(IOError):
	pass

class NotExistsError(FileSystemError):
	pass

class FileNotExistsError(NotExistsError):
	pass

class DirectoryNotExistsError(NotExistsError):
	pass

class DirectoryNotEmptyError(FileSystemError):
	pass

class FileSystemInformation(object):
	def __init__(self, fullPath, lastModified, size):
		self.fullPath = fullPath
		if isinstance(lastModified, basestring):
			self.lastModified = dateutil.parser.parse(lastModified)
		else:
			self.lastModified = lastModified
		self.size = size

	@property
	def name(self):
		return os.path.basename(self.fullPath)

	def __unicode__(self):
		return self.fullPath

class FileInformation(FileSystemInformation):
	def download(self):
		raise NotImplementedError()

	def upload(self, file):
		raise NotImplementedError()

	def delete(self):
		raise NotImplementedError()

class DirectoryInformation(FileSystemInformation):
	
	def getFiles(self):
		raise NotImplementedError()

	def getDirectories(self):
		raise NotImplementedError()

	def delete(self):
		raise NotImplementedError()

	def createDirectory(self, name):
		raise NotImplementedError()

	def createFile(self, file):
		raise NotImplementedError()

class FileSystem:
	"""
	File System API
	Defines base functions used by the API. Implement those that are needed
	"""

	def getMaxFileSize(self):
		"""
		Get the maximal file size that can be uploaded under the current file system
		"""
		return None

	def getRoot(self):
		"""
		"""
		raise NotImplementedError()