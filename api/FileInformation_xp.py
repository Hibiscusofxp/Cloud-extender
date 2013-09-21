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
	"""
	Base class for all file system information objects (files/folders)

	This includes the very most rudimentary information like file name (full name), file size, date etc.
	"""

	fullPath = None
	lastModified = None
	size = None
	parent = None

	def __init__(self, fullPath, lastModified, size, parent):
		"""
		Please initialize your classes (including FileInformation, DirectoryInformation) this way. 
		You may need to implement your own constructors for FileInformation and DirectoryInformation in order to get the necessary authentication information passed in

		To invoke the root constructor, do the following:
			super(<Your type name>, self).__init__(fullPath, lastModified, size)

		@param fullPath  the full path name to the file
		@param lastModified the string or python date of the last modification date of the object
		@param size         the size (in bytes) of the object
		"""
		self.fullPath = fullPath
		if isinstance(lastModified, basestring):
			self.lastModified = dateutil.parser.parse(lastModified)
		else:
			self.lastModified = lastModified
		self.size = size
		self.parent = parent

	@property
	def name(self):
		"""
		Gets the name of the object, without the prefix path (basename)
		"""
		return os.path.basename(self.fullPath)

	def __unicode__(self):
		return self.fullPath

	def getRelativePath(self, rootElement = None):
		if self == rootElement or self.parent == None:
			return self.name
		return self.parent.getRelativePath(rootElement) + '/' + self.name

class FileInformation(FileSystemInformation):
	"""
	File Information and upload/download wrapper.
	"""
	def download(self):
		"""
		Download a file and return a file-like object of its contents
		"""
		raise NotImplementedError()

	def upload(self, file):
		"""
		Upload to the current file the file-like object's content in "file".

		The upload may modify the file object, say certain keys. In these cases, they should be reflected as well, by updating the current object
		"""
		raise NotImplementedError()

	def delete(self):
		"""
		Delete the current file
		"""
		raise NotImplementedError()
