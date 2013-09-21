import os,sys
import urllib,urllib2,requests
import json

class DirectoryInformation(FileSystemInformation):
	"""
	Directory Information and directory listing wrapper.
	"""
	def getFiles(self):
		"""
		Get files under this directory, in the form of a enumerable list of FileInformation

		@return enumerable of FileInformation
		"""
		raise NotImplementedError()

	def getDirectories(self):
		"""
		Get directories under this directory, in the form of a enumerable list of DirectoryInformation\

		@return enumerable of DirectoryInformation
		"""
		raise NotImplementedError()

	def delete(self):
		"""
		Delete this directory
		"""
		raise NotImplementedError()

	def createDirectory(self, name):
		"""
		Create a directory under the current directory. 

		@param the name of the new directory. Technically, there shouldn't be slashes or backslashes in the name
		@return the newly created directory in the format of a DirectoryInformation
		"""
		raise NotImplementedError()

	def createFile(self, name, file):
		"""
		Create a new file and load it with the data in file.

		@param  file the file-like object that holds the contents of the new file to be created
		@return the newly uploaded FileInformation
		"""
		raise NotImplementedError()