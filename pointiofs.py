from api import fs
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

def table2dict(pointioTbl):
	headers = pointioTbl['RESULT']['COLUMNS']
	data    = pointioTbl['RESULT']['DATA']

	for row in data:
		yield dict(zip(headers, row))

def numstr(field):
	return unicode(int(field) if isinstance(field, float) else field)


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
	filesystem = None
	fileID = None
	session = requests

	def __init__(self, filesystem, fullPath = None, lastModified = None, size = None, parent = None, fileID = ''):
		super(FileInformation, self).__init__(fullPath, lastModified, size, parent)
		self.filesystem = filesystem
		if filesystem.session:
			self.session = filesystem.session
		self.fileID = fileID

	@property
	def filename(self):
		return self.name

	def download(self):
		"""
		Download a file and return a file-like object of its contents
		"""
		paras = {
			'folderid': self.filesystem.folderID.encode('utf-8'),
			'filename': self.filename.encode('utf-8'),
			'fileid': self.fileID.encode('utf-8'),
			'containerid': self.parent.containerID.encode('utf-8'),
			'remotepath': self.parent.originalPath.encode('utf-8'),
		}
		paras = urllib.urlencode(paras)
		res = self.session.get(
			"https://api.point.io/v2/folders/files/download.json?"+paras,
			headers={
				'Authorization': self.filesystem.authorization,
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
			'folderid': self.filesystem.folderID,
			'filename': self.filename,
			# if filename is different, a new file will be uploaded
			'fileid': self.fileID,
			'containerid': self.parent.containerID,
			'remotepath': self.parent.originalPath,
			#'filecontents': filecontents
		}
		req = self.session.post(
			"https://api.point.io/v2/folders/files/upload.json",
			headers= {'Authorization': self.filesystem.authorization},
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
			'folderid': self.filesystem.folderID,
			'filename': self.filename,
			'fileid': self.fileID,
			'containerid': self.parent.containerID,
			'remotepath': self.parent.originalPath
		}
		res = self.session.post(
			"https://api.point.io/v2/folders/files/delete.json", data=paras,
			headers={
				'Authorization': self.filesystem.authorization,
			})
		res.close()


class DirectoryInformation(fs.DirectoryInformation):
	url_list = 'https://api.point.io/v2/folders/list.json'
	url_create = 'https://api.point.io/v2/folders/create.json'
	session = requests
	containerID = None
	originalPath = None
	filesystem = None


	json_cache = None
	def __init__(self, filesystem, fullPath = '/', lastModified = None, size = None, parent = None, containerID = '', originalPath = ''):
		super(DirectoryInformation, self).__init__(fullPath, lastModified, size, parent) 

		self.filesystem = filesystem
		if filesystem.session:
			self.session = filesystem.session
		self.containerID = containerID
		self.originalPath = originalPath

	def delete(self):
		pass

	def getJSONResult(self, refresh=False):
		if not self.json_cache or refresh:
			query_args = { 
				'folderId': self.filesystem.folderID.encode('utf-8'), 
				'containerid': self.containerID.encode('utf-8'), 
				'path': self.originalPath.encode('utf-8')  
			}
			data = urllib.urlencode(query_args)
			res = self.session.get(self.url_list + "?" + data, 
				headers = {
					"Authorization": self.filesystem.authorization
				})
			
			self.json_cache = res.json()
		return self.json_cache

	def getFiles(self, refresh=False):
		py = self.getJSONResult(refresh)

		for item in table2dict(py):
			if (item["TYPE"] != "DIR"):
				fullPath = item["PATH"].rstrip('/') + '/' + item["NAME"]
				t = item['MODIFIED'].split("'")[1]
				lastModified = t + " GMT"
				size = item['SIZE']
				fileid = numstr(item['FILEID'])
				yield FileInformation(
					self.filesystem, parent = self,
					fullPath = fullPath, lastModified = lastModified,
					size = size, fileID = fileid)

	def getDirectories(self, refresh = False):
		py = self.getJSONResult(refresh)
		# folderid, authorization, parent
		for item in table2dict(py):
			if (item["TYPE"] == "DIR"):
				path = item["NAME"]
				fullPath = item["PATH"].rstrip('/')
				t = item["MODIFIED"].split("'")[1]
				lastModified = t + " GMT"
				size = item['SIZE']
				fileid = numstr(item['FILEID'])
				containerid = numstr(item['CONTAINERID'])
				yield DirectoryInformation(
					self.filesystem, fullPath = fullPath, parent = self, 
					lastModified = lastModified, size = size, 
					containerID = containerid, originalPath = item['PATH'])

	def createDirectory(self, name):
		foldername = name
		if self.filesystem.storageTypeID == 19: #Dropbox
			foldername = self.fullPath + "/" + name
		query_args = { 'folderId': self.filesystem.folderID, 'foldername': foldername, 'containerid': self.containerID }
		res = self.session.post(self.url_create, data = query_args, 
			headers = {
				"Authorization": self.filesystem.authorization
			})

		res.close()

		path = self.fullPath + "/" + name
		
		py = self.getJSONResult(True)
		for item in table2dict(py):
			if (item["NAME"].strip('/').lower() == name.lower()):
				containerid = numstr(item['CONTAINERID'])
				originalpath = item['PATH']

		assert(containerid != None)

		#Get lastMod and size from response
		return DirectoryInformation(self.filesystem, fullPath=path, 
			parent=self, containerID = containerid, originalPath = originalpath)

	def createFile(self, name, file):
		fnFull = self.fullPath + '/' + name
		newFile = FileInformation(self.filesystem, fullPath = fnFull, 
			parent = self, fileID = name)
		newFile.upload(file);
		# CAUTION: fileid might not correct now!
		# remaining: grab the fileid
		fileList = self.getFiles(True)
		for item in fileList:
			if (item.filename == name):
				return item
		return newFile


class FileSystem(fs.FileSystem):
	rootDir = '/'
	folderID = None
	authorization = None
	session = None
	storageTypeID = None

	def __init__(self, folderID, authorization, storageTypeID, rootDir = '/'):
		self.folderID = folderID
		self.authorization = authorization
		self.session = requests.session()
		self.rootDir = rootDir.replace("\\","/")
		self.storageTypeID = storageTypeID

	def getRoot(self):
		rootDir = DirectoryInformation(self)
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


