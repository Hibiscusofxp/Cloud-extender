import os,sys
import urllib,urllib2,requests
import json

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