from .api import fs
#import fs
import os
import os.path
import stat
import datetime
import shutil
import urllib,urllib2,requests
import json
import yaml
import dateutil

class RequestFileWrapper:
	def __init__(self, res):
		self.response = res
		self.read_iter = iter(res.iter_content(4096))

	def read(self, size):
		try:
			return self.read_iter.next()
		except StopIteration:
			return ''

	def close(self):
		self.response.close()

class FileInformation(fs.FileInformation):
	authorization = None
	folderid = None
	filename = None
	fileid = None
	session = requests

	def __init__(self, fullPath, lastModified, size, parent, authorization, folderid, fileid, containerid, remotepath):
		super(FileInformation, self).__init__(fullPath, lastModified, size, parent)
		self.authorization = authorization
		self.filename = self.name
		self.folderid = folderid
		self.fileid = fileid
		self.containerid = containerid
		self.remotepath = remotepath


	def download(self):
		"""
		Download a file and return a file-like object of its contents
		"""
		paras = {
			'folderid': self.folderid,
			'filename': self.filename.encode('utf-8'),
			'fileid': self.fileid.encode('utf-8'),
			'containerid': self.containerid.encode('utf-8'),
			'remotepath': self.remotepath.encode('utf-8'),
		}
		paras = urllib.urlencode(paras)
		res = self.session.get(
			"https://api.point.io/v2/folders/files/download.json?"+paras,
			headers={
				'Authorization': self.authorization,
			})
		res = res.json()
		resURL = res['RESULT']
		return RequestFileWrapper(self.session.get(resURL, stream=True))
		#example: result = cld.DownloadFile(cld.sessionkey, r"64B367EA-286D-481F-92DD9E28E9B3B4C1", "JustATest.txt", "10529642791")

	def upload(self, file):
		files = {'filecontents': file}
		#folderid = folderidVal
		#filename = filenamjson.loads
		# newfileid = self.filename
		# CAUTION: filename will not change to be the uploaded file name
		filecontents = files
		data = {
			'folderid': self.folderid,
			'filename': self.filename,
			# if filename is different, a new file will be uploaded
			'fileid': self.fileid,
			'containerid': self.containerid,
			'remotepath': self.remotepath,
			#'filecontents': filecontents
		}
		req = self.session.post(
			"https://api.point.io/v2/folders/files/upload.json",
			headers= {'Authorization': self.authorization},
			files = files,
			data = data
		)

		res = req.json()
		# error exception
		# update lastModified
		rawTime = res['INFO']['DETAILS']['RESULT']['MODIFIED']
		time = rawTime.split("'")[1]
		self.lastModified = dateutil.parser.parse(time + " GMT")
		# update size
		self.size = res['INFO']['DETAILS']['RESULT']['SIZE']
		# CAUTION: fileID might not be correct after upload! leave it to DirInfo class
		# no further upload or delete!

	def delete(self):
		paras = {
			'folderid': self.folderid,
			'filename': self.filename,
			'fileid': self.fileid,
			'containerid': self.containerid,
			'remotepath': self.remotepath
		}
		res = self.session.post(
			"https://api.point.io/v2/folders/files/delete.json", data=paras,
			headers={
				'Authorization': self.authorization,
			})
		res.close()

	def setSession(self, session):
		self.session = session
		return self

class DirectoryInformation(fs.DirectoryInformation):
	url_list = 'https://api.point.io/v2/folders/list.json'
	url_create = 'https://api.point.io/v2/folders/create.json'
	session = requests
	json_cache = None
	def __init__(self, folderid, authorization, path, parent = None, lastModified = None, size = None, containerid = None, originalpath = ''):
		super(DirectoryInformation, self).__init__(path, lastModified, size, parent) 

		self.folderid = folderid
		self.authorization = authorization
		self.containerid = containerid
		self.originalpath = originalpath
		
	def getJSONResult(self):
		if not self.json_cache:
			query_args = { 'folderId':self.folderid.encode('utf-8'), 'containerid': self.containerid.encode('utf-8'), 'path': self.originalpath.encode('utf-8')  }
			data = urllib.urlencode(query_args)
			res = self.session.get(self.url_list + "?" + data, 
				headers = {
					"Authorization": self.authorization
				})
			
			self.json_cache = res.json()
		return self.json_cache

	def getFiles(self):
		py = self.getJSONResult()

		for item in py["RESULT"]["DATA"]:
			if (item[2] != "DIR"):
				fullPath = item[4] + item[1]
				t = item[7].split("'")[1]
				lastModified = t + " GMT"
				size = item[8]
				# fileid = item[0]
				fileid = unicode(int(item[0]) if isinstance(item[0], float) else item[0])
				yield FileInformation(fullPath, lastModified, size, self, self.authorization, self.folderid, fileid, self.containerid, self.originalpath).setSession(self.session)

	def getDirectories(self):
		py = self.getJSONResult()
		# folderid, authorization, parent
		for item in py["RESULT"]["DATA"]:
			if (item[2] == "DIR"):
				path = item[1]
				fullPath = item[4].rstrip('/')
				t = item[7].split("'")[1]
				lastModified = t + " GMT"
				size = item[8]
				# fileid = item[0]
				fileid = unicode(int(item[0]) if isinstance(item[0], float) else item[0])
				containerid = unicode(int(item[3]) if isinstance(item[3], float) else item[3])
				yield DirectoryInformation(self.folderid, self.authorization, fullPath, self, lastModified, size, containerid, item[4]).setSession(self.session)

	def createDirectory(self, name):
		query_args = { 'folderId':self.folderid, 'foldername':name, 'containerid': self.containerid }
		res = self.session.post(self.url_create, data = query_args, 
			headers = {
				"Authorization": self.authorization
			})

		res.close()

		path = self.fullPath + "/" + name
		# list the files
		query_args = { 'folderId':self.folderid.encode('utf-8'), 'containerid': self.containerid }
		data = urllib.urlencode(query_args)
		res = self.session.get(self.url_list + "?" + data, 
			headers = {
				"Authorization": self.authorization
			})
		
		containerid = None
		py = res.json()
		for item in py["RESULT"]["DATA"]:
			if (item[1].strip('/').lower() == name.lower()):
				containerid = unicode(int(item[3]) if isinstance(item[3], float) else item[3])
				originalpath = item[4]

		assert(containerid != None)

		#Get lastMod and size from response
		return DirectoryInformation(self.folderid, self.authorization, path, self, None, None, containerid, originalpath).setSession(self.session)	

	def createFile(self, name, file):
		fnFull = os.path.join(self.fullPath, name)		
		newFile = FileInformation(fnFull, "", 0, self.parent, self.authorization, self.folderid, name, self.containerid, self.originalpath).setSession(self.session)
		newFile.upload(file);
		# CAUTION: fileid might not correct now!
		# remaining: grab the fileid
		fileList = self.getFiles()
		for item in fileList:
			if (item.filename == name):
				newFile.fileid = item.fileid
		return newFile

	def setSession(self, session):
		self.session = session
		return self

class FileSystem(fs.FileSystem):
	rootDir = '/'
	folderid = None
	authorization = None
	session = None
	def __init__(self, folderid, authorization, rootDir = '/'):
		self.folderid = folderid
		self.authorization = authorization
		self.session = requests.session()
		self.rootDir = rootDir.replace("\\","/")


	def getRoot(self):
		rootDir = DirectoryInformation(self.folderid, self.authorization, '/', None, None, None, '').setSession(self.session)
		workingDir = rootDir
		for segment in self.rootDir.split("/"):
			if segment == "":
				continue

			resultList = [dir for dir in workingDir.getDirectories() if dir.name.lower() == segment.lower()]
			if len(resultList) > 0:
				workingDir = resultList[0]
				continue

			workingDir = workingDir.createDirectory(segment)

		workingDir.parent = None
		return workingDir


