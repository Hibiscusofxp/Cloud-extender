from .api import fs
import os
import os.path
import stat
import datetime
import shutil

class FileInformation(fs.FileInformation):
	authorization = None
	folderid = None
	filename = None
	fileid = None

	def __init__(self, fullPath, lastModified, size, parent, parent, authorization, folderid, fileid):
		self.fullPath = fullPath
		self.lastModified = lastModified
		self.size = size
		self.parent = parent
		self.authorization = authorization
		self.filename = self.name
		stats = os.stat(path)
		super(FileInformation, self).__init__(path, datetime.datetime.fromtimestamp(stats[stat.ST_CTIME]), stats[stat.ST_SIZE], parent)

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
				'Authorization': authorization,
			})
		req = urllib2.urlopen(reque)
		return req
		#example: result = cld.DownloadFile(cld.sessionkey, r"64B367EA-286D-481F-92DD9E28E9B3B4C1", "JustATest.txt", "10529642791")

	def upload(self, file):
		files = {'file': open(pathAndFilename, 'rb')}
		#folderid = folderidVal
		#filename = filenamjson.loads
		fileid = filename
		filecontents = files
		data = {
			'folderid': folderid,
			'filename': filename,
			'fileid': fileid,
			'filecontents': filecontents
		}
		req = requests.post(self.url+'/folders/files/upload.json',
			headers= {'Authorization': authorization},
			files = files,
			data = data
		)
		return req
		
		with open(self.fullPath, 'wb') as ofile:
			shutil.copyfileobj(file, ofile)

	def delete(self):
		os.remove(self.fullPath)