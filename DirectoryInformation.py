from .api import fs
import os
import os.path
import stat
import datetime
import shutil
import urllib,urllib2,requests
import json

class FileInformation(fs.FileInformation):
	authorization = None
	folderid = None
	filename = None
	fileid = None

	def __init__(self, fullPath, lastModified, size, parent, authorization, folderid, fileid):
		super(FileInformation, self).__init__(fullPath, lastModified, size, parent)
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
		#TODO See how to extract data from response. We need date
		#return req
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
		#return req

class DirectoryInformation(fs.DirectoryInformation):
	url_list = 'https://api.point.io/v2/folders/list.json'
	url_create = 'https://api.point.io/v2/folders/create.json'
	def __init__(self, folderid, authorization, path, parent = None, lastModified = None, size = None):
		super(DirectoryInformation, self).__init__(path, lastModified, size, parent) 

		self.folderid = folderid
		self.authorization = authorization
		

	def getFiles(self):
		query_args = { 'folderId':self.folderid }
		data = urllib.urlencode(query_args)
		request = urllib2.Request(self.url_list, data, 
			headers = {
				"Authorization": self.authorization
			})
		response = urllib2.urlopen(request)
		r = response.readline()
		py = json.loads(r)
		for item in py["RESULT"]["DATA"]:
			if (item[2] != "DIR"):
				fullPath = item[4] + item[1]
				t = item[7].split("'")[1]
				lastModified = t + " GMT"
				size = item[8]
				fileid = item[0]
				yield FileInformation(fullPath, lastModified, size, self, self.authorization, self.folderid, fileid)

	def getDirectories(self):
		query_args = { 'folderId':self.folderid }
		data = urllib.urlencode(query_args)
		request = urllib2.Request(self.url_list, data, 
			headers = {
				"Authorization": self.authorization
			})
		response = urllib2.urlopen(request)
		r = response.readline()
		py = json.loads(r)
		# folderid, authorization, parent
		for item in py["RESULT"]["DATA"]:
			if (item[2] == "DIR"):
				path = item[1]
				fullPath = item[4] + item[1]
				t = item[7].split("'")[1]
				lastModified = t + " GMT"
				size = item[8]
				fileid = item[0]
				yield DirectoryInformation(self.folderid, self.authorization, fullPath, self, lastModified, size)

	def createDirectory(self, name):
		query_args = { 'folderId':self.folderid, 'foldername':name }
		data = urllib.urlencode(query_args)
		request = urllib2.Request(self.url_create, data, 
			headers = {
				"Authorization": self.authorization
			})
		response = urllib2.urlopen(request)
		path = path + "/" + name

		#Get lastMod and size from response
		return DirectoryInformation(self.folderid, self.authorization, path, self)		

	def createFile(self, name, file):
		fnFull = os.path4join(self.fullPath, name)
		shutil.copyfileobj(file, open(fnFull, 'wb'))
		return FileInformation(fnFull, self)

class FileSystem(fs.FileSystem):
	rootDir = '/'
	folderid = None
	authorization = None
	def __init__(self, folderid, authorization):
		self.folderid = folderid
		self.authorization = authorization
	def getRoot(self):
		return DirectoryInformation(self.folderid, self.authorization, self.rootDir, None, None, None)
