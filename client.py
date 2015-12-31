from libcontractvm import Wallet, WalletNode, ConsensusManager
from forumdapp import ForumManager
import sys, config
consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")
walletA=WalletNode.WalletNode (chain='XLT', url=config.WALLET_NODE_URL, wallet_file='data/walletA.wallet')
walletB=WalletNode.WalletNode (chain='XLT', url=config.WALLET_NODE_URL, wallet_file='data/walletB.wallet')
foManA = ForumManager.ForumManager (consMan, wallet=walletA)  
foManB = ForumManager.ForumManager (consMan, wallet=walletB)  
title = "titolo del post di A"
postMessage = "messaggio di A"

try:
    postA = foManA.addPost ( title, postMessage)
    foManA.getList()
except:
    print ('Error.')

titleB = "titolo di B"
postMessageB = "messaggio di B"

try:
    postB= foManB.addPost ( titleB, postMessageB)
except:
    print ('ErrorB.')
try:
	comment = foManA.addComment(postA, "this is a comment")
	commentB = foManB.addComment(postB, "this is a comment B")
except:
	print('error on comments')



