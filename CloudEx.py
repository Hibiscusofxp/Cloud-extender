import os,sys
import urllib,urllib2,requests

class CloudEx:
	"""CloudExtender Project in MHacks
	"""
	email = r"hibiscusofxp@gmail.com"
	password = "cloudextender"
	apikey = r"91CE19E5-D328-467F-BC22733ADE7E51AF"
	appSecret = "yOlAJ1t9SNSxCLuTH5QZs8ZXtv9xvkigirKFJHn46Ml6uuTkgmBFgaQyWfuKoSU"
	url = r"https://api.point.io/v2"
	sessionkey = "FA35E8D7EA649C8B96F7B73E61D15D9BA5A944433BD29646993EAC04A8597C889B9E530C7FA11F766462A7FE5E8F3A1CF0E3DEDC681B7ABED7433AD78C5178C4"
	siteTypeId = 0
	def Auth(self):
		fullurl = self.url + r"/auth.json"
		paras = {
			'email':self.email,
			'password':self.password,
			'apikey':self.apikey
		}
		paras = urllib.urlencode(paras)
		result = urllib.urlopen(fullurl, paras)
		arr = result.readlines()
		arr = eval(arr[0])
		self.sessionkey = arr['RESULT']['SESSIONKEY']
		return result
	def GetStorageList(self):
		reque = urllib2.Request(
			"https://api.point.io/v2/storagetypes/list.json",
			headers={
				"Authorization": self.sessionkey
			})
		req = urllib2.urlopen(reque)
		# self.siteTypeId = 15
		return req
	def GetSiteParas(siteID):
		# do on http://point.io/tutorial!!!!
		self.siteTypeId = siteID
		reque = urllib2.Request(
			"%s%d%s"%("https://api.point.io/v2/storagetypes/", siteId,"/params.json"),
			headers={
				"Authorization": self.sessionkey
			})
		req = urllib2.urlopen(reque)
		return req
	def CreateNewStorage(siteID):
		# do on http://point.io/tutorial!!!!