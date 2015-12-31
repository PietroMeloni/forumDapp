# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from contractvmd import config, dapp, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)

class ForumProto:
	DAPP_CODE = [ 0x01, 0x04 ]
	METHOD_NEW_POST = 0x01
	METHOD_NEW_COMMENT = 0x02
	METHOD_GET_POSTS = 0x03
	METHOD_LIST = [METHOD_NEW_POST, METHOD_NEW_COMMENT]


class NewPostMessage (message.Message):
	def addPost (title, postMessage):
		m = NewPostMessage()
		m.title = title
		m.postMessage = postMessage
		m.DappCode = ForumProto.DAPP_CODE
		m.MethodCode = ForumProto.METHOD_NEW_POST
		return m
	def toJSON (self):
		data = super (NewPostMessage, self).toJSON ()
		if self.Method == ForumProto.METHOD_NEW_POST:
			data["title"] = self.title
			data["postMessage"] = self.postMessage
		else:
			return None

		return data

class NewCommentMessage(message.Message):
	def addComment (postID, textComment):
		m = NewPostMessage()
		m.postID = postID
		m.textComment = textComment
		m.DappCode = ForumProto.DAPP_CODE
		m.MethodCode = ForumProto.METHOD_NEW_COMMENT
		return m
	def toJSON (self):
		data = super (NewCommentMessage, self).toJSON ()
		if self.Method == ForumProto.METHOD_NEW_POST:
			data["postID"] = self.Title
			data["comment"] = self.PostMessage
		else:
			return None

		return data


class ForumAPI (dapp.API):
	def __init__ (self, core, dht, api):
		self.api = api
		

		rpcmethods = {}

		rpcmethods["getPosts"] = {
			"call": self.method_getPosts,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["addPost"] = {
			"call": self.method_addPost,
			"help": {"args": [ "title", "postMessage"], "return": {}}
		}
		
		rpcmethods["addComment"] = {
			"call": self.method_addComment,
			"help": {"args": ["postID", "comment"], "return": {}}
		}
		errors = {}

		super (ForumAPI, self).__init__(core, dht, rpcmethods, errors)
		
	def method_getPosts (self):
		return self.core.getPosts ()

	def method_addPost (self, title, postMessage):
		msg = NewPostMessage.addPost ( title, postMessage)
		return self.createTransactionResponse (msg)

	def method_addComment (self, postID, comment):
		msg = NewCommentMessage.addComment (postID, comment)
		return self.createTransactionResponse (msg)

class ForumCore (dapp.Core):
	def __init__ (self, chain, database):
		database.init ('posts', [])
		database.init ('comments',[])
		super (ForumCore, self).__init__ (chain, database)
	
	def addPost (self,postID, title, postMessage):
		self.database.listappend ('posts', { 'postID':postID,'title': title, 'postMessage': postMessage})
					
	def addComment (self,postID, comment):
		self.database.listappend ('comments', {'postID': postID, 'comment': comment})	
	
	def getPosts(self):
		return self.database.get ('posts')

class forumdapp (dapp.Dapp):
	def __init__ (self, chain, db, dht, apimaster):
		self.core = ForumCore (chain, db)
		api = ForumAPI (self.core, dht, apimaster)		
		super (forumdapp, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, api)
		
	def handleMessage (self, m):
		if m.Method == ForumProto.METHOD_NEW_POST:
			logger.pluginfo ('Found new post %s: the Title is %s', m.Hash, m.Data['title'])
			self.core.addPost (m.Hash, m.Data['title'], m.Data['postMessage'])
