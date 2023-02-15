#!/usr/bin/env python3

import time
import subprocess
import copy
from hexbytes import HexBytes

from console import *
from aux import TCP_mp, TCP_server, TCP_server2, l2d

global peered, peers, peers_geth
peers = dict()
peers_geth = []
peered = set()

def getEnodes():
    return [peer['enode'] for peer in w3.geth.admin.peers()]

def getIps(__enodes = None):
    if __enodes:
        return [enode.split('@',2)[1].split(':',2)[0] for enode in __enodes]
    else:
        return [enode.split('@',2)[1].split(':',2)[0] for enode in getEnodes()]

def peering():
	""" Control routine for robot-to-robot dynamic peering """
	global peered, peers, peers_geth
	
	peers_geth_enodes = getEnodes()
	peers_geth = set(getIps(peers_geth_enodes))

	for peer in peers:
		if peers[peer] not in peered:
			enode = tcp_enode.request(host=peers[peer], port=5000) 
			if 'enode' in enode:
				w3.geth.admin.addPeer(enode)
				peered.add(peers[peer])
				print('Added peer: %s|%s' % (peer, enode))

	temp = copy.copy(peered)

	for peer in temp:
		if peer not in peers.values():
			enode = tcp_enode.request(host=peer, port=5000)
			if 'enode' in enode:
				w3.provider.make_request("admin_removePeer",[enode])
				peered.remove(peer)
				print('Removed peer: %s|%s' % (peer, enode))

	peers = dict()
	tcp_peering.setData(len(peers_geth))


def blockHandle():
	""" Every time new blocks are synchronized """

	pass

	tcp_calls.setData({})

if __name__ == '__main__':

	w3 = init_web3()
	sc = registerSC(w3)
	bf = w3.eth.filter('latest')

################################################################################################################
### TCP for peering ###
################################################################################################################

	data = len(peers_geth)
	host = subprocess.getoutput("ip addr | grep 172.18.0. | tr -s ' ' | cut -d ' ' -f 3 | cut -d / -f 1")
	port = 9898    

	tcp_peering = TCP_server2(data, host, port)
	tcp_peering.start()   

################################################################################################################
### TCP for calls ###
################################################################################################################

	# data = ""
	# port = 9899    

	# tcp_calls = TCP_mp(data, host, port)
	# tcp_calls.start()   

	# blockHandle()

################################################################################################################
### TCP for enodes ###
################################################################################################################

	data = w3.enode
	host = getIps([w3.enode])[0]
	port = 5000

	tcp_enode = TCP_server(w3.enode, host, port, unlocked = True)
	tcp_enode.start()

################################################################################################################

	while True:

		peers = tcp_peering.getNew()
		print(peers)
		if peers:
			peering()

		# newBlocks = bf.get_new_entries()
		# if newBlocks:
		# 	blockHandle()

		time.sleep(0.25)