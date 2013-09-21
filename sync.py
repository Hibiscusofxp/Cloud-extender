"""
Synchronization Implementation
"""

from .api import fs
import os
import os.path

import shutil

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

class MultiSynchronizer:
	local = None
	remotes = []
	def __init__(self, localFS, remoteFSs):
		self.local = localFS
		self.remotes = remoteFSs

	def synchronize(self):
		print "Loading local file list"
		localList, localSize = loadFSDict(self.local)

		print "Loading remote file lists"

		remoteLists = []
		remoteSizes = []

		for remote in self.remotes:
			print "Loading %s" % (remote,)
			lst, sz = loadFSDict(remote)
			remoteLists.append(lst)
			remoteSizes.append(sz)

		downloads = {}
		uploads = {}
		deletions = {} #Usedly currently only when there is a conflict between the file systems.

		print "Resolving changes"

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
					print obj.lastModified, targetFound.lastModified
					uploads[path] = (obj, targetFound, listFound)

		print uploads

		print "Downloading"
		for path, obj in downloads.iteritems():
			print "Downloading %s" % (path,)
			makedirs(localList, os.path.dirname(path))
			dlObj = obj.download()
			if path in localList:
				localList[path].upload(dlObj)
			else:
				localList[os.path.dirname(path)].createFile(os.path.basename(path), dlObj)


		print "Uploading"
		for path, obj in uploads.iteritems():
			print "Uploading %s" % (path,)
			obj, remoteObj, remoteList = obj
			if remoteObj:
				remoteObj.upload(obj.download())
			else:
				remoteList = remoteLists[getSortedDictList(remoteSizes)[0]['index']]
				makedirs(localList, os.path.dirname(path))
				remoteList[os.path.dirname(path)].createFile(os.path.basename(path), obj.download())

