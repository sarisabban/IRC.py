#!/usr/bin/python3

import socket , re , datetime , threading , time

#IRC Information
SERVER 		= 'irc.freenode.net'
PORT 		= 6667
NICKNAME 	= 'write nickname here'
CHANNEL 	= '#write channel here'
network 	= SERVER.split('.')

#Terminal Colours
Black 	= '\x1b[30m'
Red	= '\x1b[31m'
Green	= '\x1b[32m'
Yellow	= '\x1b[33m'
Blue	= '\x1b[34m'
Purple	= '\x1b[35m'
Cyan	= '\x1b[36m'
White	= '\x1b[37m'
Cancel	= '\x1b[0m'

#Logo
print(Green + '''
╦╦═╗╔═╗  ┌─┐┬  ┬┌─┐┌┐┌┌┬┐
║╠╦╝║    │  │  │├┤ │││ │ 
╩╩╚═╚═╝  └─┘┴─┘┴└─┘┘└┘ ┴ 
''' + Cancel)
#----------------------------------------------------------------------------------------------------
#Functions:
def send_data(command):
	''' To send data to IRC '''
	IRC.send((command + '\n').encode())

def send_txt():
	''' To send text to IRC '''
	text = input()
	IRC.send(('PRIVMSG ' + CHANNEL + ' :' + text + '\r\n').encode())
	#print(Cyan + datetime.datetime.now().strftime('%H:%M') + Purple + '\t' + text + Cancel)

def Connection():
	''' Maintian Connection and listen for incoming text'''
	while True:
		buffer = IRC.recv(1024)
		msg = buffer.decode().split()
		#print(msg)
		if msg[1] == 'NOTICE':
			print('\x1b[36m' + 'Calling' + msg[0] + '\x1b[0m')
			server_a = msg[0].split(':')
			server_b = server_a[1]
		if msg[1] == '433':
			print(Red + '[-] Nickname already in use, try a different one' + Cancel)
			break
		if msg[1] == 'JOIN':
			print(Yellow + '---------------------------')
			print('\tCONNECTED')
			print('Network:\t' , network[1] , '\nServer:\t\t' , server_b , '\nChannel:\t' , msg[2])
			print('---------------------------' + Cancel)
		if msg[0] == 'PING': #When server pings answer with pong to maintain connection
			server1 = msg[1].split(':')
			server2 = server1[1]
			send_data('PONG %s' % server2)
			#print('Received' , msg[0] , 'from' , msg[1] , 'Sent back:' , 'PONG')
		#Receive Text
		if msg[1] == 'PRIVMSG':
			if any(['ThisISaBoT' in m for m in msg]):
				text = ' '.join(msg[3 : ])
				text = text.strip(':')
				nick1 = msg[0].split('!')
				nick2 = nick1[0].split(':')
				print(Cyan + datetime.datetime.now().strftime('%H:%M') + '\t' + Red + nick2[1] , '\t' , text + Cancel)

			else:
				text = ' '.join(msg[3 : ])
				text = text.strip(':')
				nick1 = msg[0].split('!')
				nick2 = nick1[0].split(':')
				print(Cyan + datetime.datetime.now().strftime('%H:%M') + Cancel + '\t' + nick2[1] , '\t' , text)
#----------------------------------------------------------------------------------------------------
#Connect To IRC
IRC = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
IRC.connect((SERVER , PORT))
send_data('USER user host server name')
send_data('NICK ' + NICKNAME)
send_data('JOIN ' + CHANNEL)

#MainTain Connection and Receive Text
t1 = threading.Thread(target = Connection)
t1.daemon = True
t1.start()

#Send User Text
while True:
	send_txt()
