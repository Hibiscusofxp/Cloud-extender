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
	pass

class DirectoryInformation(FileSystemInformation):
	pass

class FileSystem:
	"""
	File System API
	Defines base functions used by the API. Implement those that are needed
	"""

	def getFiles(self, path):
		"""
		Return a list or iterable of files under path
		Each item in the list should be of type FileInformation
		"""
		raise NotImplementedError()

	def getDirectories(self, path):
		"""
		Return a list or iterable of directories under path
		Each item in the list should be of type DirectoryInformation
		"""
		raise NotImplementedError()

	def getFileInfo(self, path):
		"""
		Return a single element of the file being pointed to by path
		The single element should be of type FileInformation
		"""
		raise NotImplementedError()

	def getMaxFileSize(self):
		"""
		Get the maximal file size that can be uploaded under the current file system
		"""
		return None

	def downloadFile(self, path):
		"""
		Download the file under path given by path, and return a file-like object (which at least provides .read(size) which reads into a str buffer)
		"""
		raise NotImplementedError()

	def uploadFile(self, path, file):
		"""
		Upload the file-like object under file to the path given by path.
		"""
		raise NotImplementedError()

	def createDirectory(self, path):
		"""
		Creates a directory under path
		"""
		raise NotImplementedError()

	def fileExists(self, path):
		"""
		Checks if path exists as a file, and return a boolean value that indicates this state
		"""
		raise NotImplementedError()

	def directoryExists(self, path):
		"""
		Checks if a path exists as a directory, and return a boolean value that indicates this state
		"""
		raise NotImplementedError()

	def deleteDirectory(self, path):
		"""
		Delete the directory under path
		"""
		raise NotImplementedError()

	def deleteFile(self, path):
		"""
		Delete the file under path
		"""
		raise NotImplementedError()