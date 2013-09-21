from .api import fs
import os
import os.path
import stat
import datetime
import shutil

class DirectoryInformation(fs.DirectoryInformation):
	folderid = None
	authorization = None
	parent = None
	def __init__(self, folderid, authorization, parent):
		url_list = 'https://api.point.io/v2/folders/list.json'
		self.folderid = folderid
		self.authorization = authorization
		self.parent = parent
		# stats = os.stat(path)
		# super(DirectoryInformation, self).__init__(path, datetime.datetime.fromtimestamp(stats[stat.ST_CTIME]), stats[stat.ST_SIZE], parent)
		#
	def getFiles(self):
		query_args = { 'folderId':folderid }
		data = urllib.urlencode(query_args)
		request = urllib2.Request(self.url, data, 
			headers = {
				"Authorization": self.authorization
			})
		response = urllib2.urlopen(request)
		r = response.readline()
		py = json.loads(r)
		for item in py["RESULT"]["DATA"]:
			if (item[2] != "DIR")
				fullPath = item[1] + item[4]
				lastModified = item[7]
				size = item[8]
				fileid = item[0]
				yield FileInformation(fullPath, lastModified, size, self.parent, self.authorization, self.folderid, fileid)
		# for fn in os.listdir(unicode(self.fullPath)):
		# 	fnFull = os.path.join(self.fullPath, fn)
		# 	if os.path.isfile(fnFull):
		# 		# yield FileInformation(fnFull, self)
	def getDirectories(self):
		query_args = { 'folderId':folderid }
		data = urllib.urlencode(query_args)
		request = urllib2.Request(self.url, data, 
			headers = {
				"Authorization": self.authorization
			})
		response = urllib2.urlopen(request)
		r = response.readline()
		py = json.loads(r)
		# folderid, authorization, parent
		for item in py["RESULT"]["DATA"]:
			if (item[2] == "DIR")
				fullPath = item[1] + item[4]
				lastModified = item[7]
				size = item[8]
				fileid = item[0]
				yield DirectoryInformation(self.folderid, self.authorization, self)
	# def delete(self):
		# os.remove(self.fullPath)

	def createDirectory(self, name):
		os.mkdir(os.path.join(self.fullPath,name))
		return DirectoryInformation(os.path.join(self.fullPath, name), self)

	def createFile(self, name, file):
		fnFull = os.path.join(self.fullPath, name)
		shutil.copyfileobj(file, open(fnFull, 'wb'))
		return FileInformation(fnFull, self)
