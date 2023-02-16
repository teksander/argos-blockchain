#!/usr/bin/env python3
import socket
import time
import subprocess
from console import *
import threading
import copy

from aux import TCP_server

class TCP_server2(object):
	""" Set up TCP_server on a background thread
	The __hosting() method will be started and it will run in the background
	until the application exits.
	"""

	def __init__(self, data, host, port):
		""" Constructor
		:type data: str
		:param data: Data to be sent back upon request
		:type ip: str
		:param ip: IP address to host TCP server at
		:type port: int
		:param port: TCP listening port for enodes
		"""
		
		self.data = str(data).encode()
		self.host = host
		self.port = port  

		self.__received = []                            
		self.__stop = False

		logger.info('TCP-Server OK')

	def __hosting(self):
		""" This method runs in the background until program is closed """ 

		 # create a socket object
		__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		# set important options
		__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# bind to the port
		__socket.bind((self.host, self.port))
		# listen on the port
		__socket.listen()

		print('TCP Server OK')  

		while True:

			if self.__stop:
				__socket.close()
				break 

			else:
				# establish a connection
				__clientsocket, addr = __socket.accept()   

				# read the data
				data = __clientsocket.recv(1024)
				if data:
					self.__received = eval(data)
				else:
					self.__received = []

				# reply to data
				__clientsocket.send(self.data)


	def getNew(self):
		if self.__stop:
			return None
			print('TCP is OFF')
		else:
			return self.__received

	def setData(self, data):
		self.data = str(data).encode()    

	def request(self, host, port):
		msg = ""

		try:
			""" This method is used to request data from a running TCP server """
			# create the client socket
			__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			# set the connection timeout
			__socket.settimeout(5)
			# connect to hostname on the port
			__socket.connect((host, port))                               
			# Receive no more than 1024 bytes
			msg = __socket.recv(1024)  
			msg = msg.decode('ascii') 
			__socket.close()

		except:
			print('TCP connection failed')

		return msg


	def start(self):
		""" This method is called to start __hosting a TCP server """
		if self.__stop:
			print('TCP Server already ON')  

		else:
			# Initialize background daemon thread
			thread = threading.Thread(target=self.__hosting, args=())
			thread.daemon = True 

			# Start the execution                         
			thread.start()   

	def stop(self):
		""" This method is called before a clean exit """   
		self.__stop = True
		print('TCP is OFF') 


def getEnodes():
    return [peer['enode'] for peer in w3.geth.admin.peers()]

def getEnodeById(__id, gethEnodes = None):
    if not gethEnodes:
        gethEnodes = getEnodes() 

    for enode in gethEnodes:
        if readEnode(enode, output = 'id') == __id:
            return enode

def getIds(__enodes = None):
    if __enodes:
        return [enode.split('@',2)[1].split(':',2)[0].split('.')[-1] for enode in __enodes]
    else:
        return [enode.split('@',2)[1].split(':',2)[0].split('.')[-1] for enode in getEnodes()]

def getIps(__enodes = None):
    if __enodes:
        return [enode.split('@',2)[1].split(':',2)[0] for enode in __enodes]
    else:
        return [enode.split('@',2)[1].split(':',2)[0] for enode in getEnodes()]



global peered, peers, peers_geth
peers = dict()
peers_geth = []
peered = set()


def buffer():
	""" Control routine for robot-to-robot dynamic peering """
	global peered, peers, peers_geth
	
	peers_geth_enodes = getEnodes()
	peers_geth = set(getIps(peers_geth_enodes))
	# print(peers_geth)

	for peer in peers:
		if peers[peer] not in peered:
			enode = tcp_enode.request(peers[peer], port) 

			if 'enode' in enode:
				w3.geth.admin.addPeer(enode)
				peered.add(peers[peer])
				print('Added peer: %s|%s' % (peer, enode))

	temp = copy.copy(peered)

	for peer in temp:
		if peer not in peers.values():
			enode = tcp.request(peer, port)
			if 'enode' in enode:
				w3.provider.make_request("admin_removePeer",[enode])
				peered.remove(peer)
				print('Removed peer: %s|%s' % (peer, enode))

	# for peer in peers_geth:
	# 	if peer not in peers.values():
	# 		enode = tcp_enode.request(peer, port)
	# 		w3.provider.make_request("admin_removePeer",[enode])
	# 		print('Removed peer: %s|%s' % (peer, enode))

	peers = dict()

if __name__ == '__main__':

	w3 = init_web3()

	data = len(peers_geth)
	host = subprocess.getoutput("ip addr | grep 172.18.0. | tr -s ' ' | cut -d ' ' -f 3 | cut -d / -f 1")
	port = 9898    

	tcp = TCP_server2(data, host, port)
	tcp.start()   
################################################################################################################

	data = w3.enode
	host = getIps([w3.enode])[0]
	port = 5000

	tcp_enode = TCP_server(w3.enode, host, port, unlocked = True)
	tcp_enode.start()

	while True:
		peers = tcp.getNew()
		if peers:
			buffer()
			tcp.setData(len(peers_geth))

		time.sleep(0.5)

