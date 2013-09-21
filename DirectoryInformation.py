import fs #
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

class DirectoryInformation(fs.DirectoryInformation):
	folderid = None
	authorization = None
	parent = None
	url_list = 'https://api.point.io/v2/folders/list.json'
	url_create = 'https://api.point.io/v2/folders/create.json'
	def __init__(self, folderid, authorization, parent):
		self.folderid = folderid
		self.authorization = authorization
		self.parent = parent
		# stats = os.stat(path)
		# super(DirectoryInformation, self).__init__(path, datetime.datetime.fromtimestamp(stats[stat.ST_CTIME]), stats[stat.ST_SIZE], parent)
		#
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
				yield FileInformation(fullPath, lastModified, size, self.parent, self.authorization, self.folderid, fileid)
		# for fn in os.listdir(unicode(self.fullPath)):
		# 	fnFull = os.path.join(self.fullPath, fn)
		# 	if os.path.isfile(fnFull):
		# 		# yield FileInformation(fnFull, self)
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
				fullPath = item[4] + item[1]
				t = item[7].split("'")[1]
				lastModified = t + " GMT"
				size = item[8]
				fileid = item[0]
				yield DirectoryInformation(self.folderid, self.authorization, self)
	# def delete(self):
		# os.remove(self.fullPath)

	def createDirectory(self, name):
		query_args = { 'folderId':self.folderid, 'foldername':name }
		data = urllib.urlencode(query_args)
		request = urllib2.Request(self.url_create, data, 
			headers = {
				"Authorization": self.authorization
			})
		response = urllib2.urlopen(request)
		r = response.readline()
		py = json.loads(r)
		# folderid, authorization, parent
		for item in py["RESULT"]["DATA"]:
			if (item[2] == "DIR"):
				fullPath = item[4] + item[1]
				lastModified = item[7]
				size = item[8]
				fileid = item[0]
				yield DirectoryInformation(self.folderid, self.authorization, self)		
		os.mkdir(os.path.join(self.fullPath,name))
		return DirectoryInformation(os.path.join(self.fullPath, name), self)

	def createFile(self, name, file):
		fnFull = os.path4join(self.fullPath, name)
		shutil.copyfileobj(file, open(fnFull, 'wb'))
		return FileInformation(fnFull, self)
