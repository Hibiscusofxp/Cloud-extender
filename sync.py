"""
Synchronization Implementation
"""

from api import fs
import os
import os.path

import shutil
import time

import config

import dateutil.tz

import threading
import Queue

def loadDirDict(dir, dct):
	size = dir.size or 0

	dct[dir.getRelativePath()] = dir
	for f in dir.getFiles():
		dct[f.getRelativePath()] = f
		size += f.size or 0

	for d in dir.getDirectories():
		size += loadDirDict(d, dct)

	return size

def loadFSDict(fs):
	dct = {}
	totalSize = loadDirDict(fs.getRoot(), dct)
	return dct, totalSize

def makedirs(dct, path):
	parts = path.split('/')
	for i in range(1, len(parts) + 1):
		partial = '/'.join(parts[0:i])
		if not partial in dct:
			newDir = dct['/'.join(parts[0:i-1])].createDirectory(parts[i-1])
			dct[partial] = newDir

def getSortedDictList(list):
	pairedDict = []
	for i in range(0,len(list)):
		pairedDict.append({'index': i, 'value': list[i]})

	return sorted(pairedDict, key=lambda x: x['value'])

def getIndexDictionary(list):
	output = {}
	for i in range(0, len(list)):
		output[id(list[i])] = i
	return output

class MultiSynchronizer:
	local = None
	remotes = []
	def __init__(self, localFS, remoteFSs):
		self.local = localFS
		self.remotes = remoteFSs

	prophet = None

	recentSizes = None

	storageTypeTranslation = {"box": 15, "drive": 19, "dropbox": 11}

	message = None
	progress = None

	progressCallback = None

	def setProphet(self,prophet):
		self.prophet = prophet

	def getSizes(self):
		if not self.recentSizes:
			return None
		return dict(zip([r.storageTypeID for r in self.remotes], recentSizes))

	def updateProgress(self, message, progress = None):
		print message
		self.message = message
		self.progress = progress

		if self.progressCallback:
			try:
				self.progressCallback()
			except:
				pass

	def setProgressCallback(self, cb):
		self.progressCallback = cb

	def synchronize(self, deletefiles = None):
		self.updateProgress("Loading file lists")

		q = Queue.Queue()
		results = []
		def remoteLoader():
			while True:
				remote = q.get()
				print "Loading %s" % (remote,)
				results.append(loadFSDict(remote))
				q.task_done()

		for i in range(5):
			t = threading.Thread(target=remoteLoader)
			t.daemon = True
			t.start()

		for remote in self.remotes:
			q.put(remote)

		localList, localSize = loadFSDict(self.local)

		q.join()

		remoteLists = []
		remoteSizes = []

		for dct, sz in results:
			remoteLists.append(dct)
			remoteSizes.append(sz)

		if config.FILE_DISTRIBUTION_MODE == 1:
			remoteListLookup = getIndexDictionary(remoteLists)

		downloads = {}
		uploads = {}
		deletions = []

		self.updateProgress("Resolving changes")

		for remoteList in remoteLists:
			for path, obj in remoteList.iteritems():
				if isinstance(obj, fs.FileInformation):
					if not path in localList or obj.lastModified > localList[path].lastModified:
						if not path in downloads:
							downloads[path] = obj

		for path, obj in localList.iteritems():
			if isinstance(obj, fs.FileInformation):
				targetFound = None
				listFound = None
				for remoteList in remoteLists:
					if path in remoteList:
						targetFound = remoteList[path]
						listFound = remoteList
						break
				if not targetFound:
					uploads[path] = (obj, None, None)
				elif obj.lastModified > targetFound.lastModified:
					uploads[path] = (obj, targetFound, listFound)

		if deletefiles:
			for path in deletefiles:
				if path in localList:
					continue
				if path in downloads:
					del downloads[path]
				for remoteList in remoteLists:
					if path in remoteList:
						deletions.append(remoteList[path])

		self.updateProgress("Downloading")
		counter = 0
		for path, obj in downloads.iteritems():
			counter += 1
			self.updateProgress("Downloading %s" % (path,), float(counter) / len(downloads) * 100)
			makedirs(localList, os.path.dirname(path))
			dlObj = obj.download()
			if path in localList:
				localList[path].upload(dlObj)
				newObj = localList[path]
			else:
				newObj = localList[os.path.dirname(path)].createFile(os.path.basename(path), dlObj)

			mtime = time.mktime(obj.lastModified.astimezone(dateutil.tz.tzlocal()).timetuple())
			os.utime(newObj.fullPath, (mtime, mtime))


		self.updateProgress("Uploading")
		counter = 0
		for path, obj in uploads.iteritems():
			counter += 1
			try:
				self.updateProgress("Uploading %s" % (path,), float(counter) / len(uploads) * 100)
				obj, remoteObj, remoteList = obj

				if remoteObj:
					if config.FILE_DISTRIBUTION_MODE == 1:
						remoteSizes[remoteListLookup[id(remoteList)]] += obj.size - remoteObj.size

					remoteObj.upload(obj.download())
					newObj = remoteObj
				else:
					sortedList = getSortedDictList(remoteSizes)

					ext = os.path.splitext(path)[1].strip('.')
					if config.FILE_DISTRIBUTION_MODE == 2 and ext != "":
						prediction = self.prophet.getPrediction(ext)["outputMulti"]
						predLookup = {}
						for pred in prediction:
							lbl = pred['label']
							if lbl.lower() in self.storageTypeTranslation:
								lbl = self.storageTypeTranslation[lbl.lower()]

							lbl = int(lbl)

							predLookup[lbl] = float(pred['score'])

						priorities = []
						for remote in self.remotes:
							if remote.storageTypeID in predLookup:
								priorities.append(predLookup[remote.storageTypeID])
							else:
								priorities.append(0)

						sortedList = getSortedDictList(priorities)
						sortedList.reverse()


					for i in range(0, len(sortedList)):
						try:
							print "Uploading to provider ID %s" % (self.remotes[sortedList[i]['index']].storageTypeID,)
							remoteList = remoteLists[sortedList[i]['index']]
							makedirs(remoteList, os.path.dirname(path))

							if config.FILE_DISTRIBUTION_MODE == 1:
								remoteSizes[remoteListLookup[id(remoteList)]] += obj.size

							newObj = remoteList[os.path.dirname(path)].createFile(os.path.basename(path), obj.download())
							break
						except Exception as ex:
							print u"Failed " + unicode(ex) + ". Switching to other providers."

				mtime = time.mktime(newObj.lastModified.astimezone(dateutil.tz.tzlocal()).timetuple())
				os.utime(obj.fullPath, (mtime, mtime))
			except Exception as ex:
				print u"Failed: " + unicode(ex)
		self.updateProgress("Deleting")

		for obj in deletions:
			self.updateProgress("Deleting %s" % (obj.fullPath))
			obj.delete()

		self.recentSizes = remoteSizes
		self.updateProgress("", 100);