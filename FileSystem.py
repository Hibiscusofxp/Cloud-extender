import os,sys
import urllib,urllib2,requests
import json

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
		get the root directory of the current file system.

		@return DirectoryInformation
		"""
		raise NotImplementedError()