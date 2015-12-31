# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import time
from libcontractvm import Wallet, ConsensusManager, DappManager

class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (ForumManager, self).__init__(consensusManager, wallet)
	def addPost (self, title, postMessage):
		cid = self.produceTransaction ('forumdapp.addPost', [ title, postMessage])
		return cid
	
	def addComment (self, postID, comment):
		cid = self.produceTransaction ('forumdapp.addComment', [ title, postMessage])
		return cid

	def getList (self):
		return self.consensusManager.jsonConsensusCall ('forum.getPosts', [])['result']
