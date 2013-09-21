from .api import fs
import os
import os.path
import stat
import datetime
import shutil
import urllib, urllib2, json, requests

class FileInformation(fs.FileInformation):
	authorization = None
	folderid = None
	filename = None
	fileid = None

	def __init__(self, fullPath, lastModified, size, parent, authorization, folderid, fileid):
		self.fullPath = fullPath
		self.lastModified = lastModified
		self.size = size
		self.parent = parent
		self.authorization = authorization
		self.filename = self.name
		self.folderid = folderid
		self.fileid = fileid

	def download(self):
		"""
		Download a file and return a file-like object of its contents
		"""
		paras = {
			'folderid': self.folderid,
			'filename': self.filename,
			'fileid': self.fileid,
		}
		paras = urllib.urlencode(paras)
		reque = urllib2.Request(
			"https://api.point.io/v2/folders/files/download.json?"+paras,
			headers={
				'Authorization': self.authorization,
			})
		req = urllib2.urlopen(reque)
		res = req.readlines()
		res = json.loads(res[0])
		resURL = res['RESULT']
		resFile = urllib.urlopen(resURL)
		return resFile
		#example: result = cld.DownloadFile(cld.sessionkey, r"64B367EA-286D-481F-92DD9E28E9B3B4C1", "JustATest.txt", "10529642791")

	def upload(self, file):
		files = {'file': file}
		#folderid = folderidVal
		#filename = filenamjson.loads
		# newfileid = self.filename
		filecontents = files
		data = {
			'folderid': self.folderid,
			'filename': self.filename,
			'fileid': self.fileid,
			'filecontents': filecontents
		}
		req = requests.post(
			"https://api.point.io/v2/folders/files/upload.json",
			headers= {'Authorization': self.authorization},
			files = files,
			data = data
		)
		return req
		# no further upload or delete!
		# CAUTION: fileID might not be correct after upload!

	def delete(self):
		paras = {
			'folderid': self.folderid,
			'filename': self.filename,
			'fileid': self.fileid,
		}
		paras = urllib.urlencode(paras)
		reque = urllib2.Request(
			"https://api.point.io/v2/folders/files/delete.json?"+paras,
			headers={
				'Authorization': self.authorization,
			})
		req = urllib2.urlopen(reque)
		return req