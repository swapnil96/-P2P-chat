#!/usr/bin/python

import socket
import os
import sys
import select

host = '10.192.40.100'
port = 10101
backlog = 10
size = 4096

def send_file(sock):
    # Function to send file

    sock.send('File name: ')
    filename = sock.recv(size)    
    file = open(filename,'rb')
    data = file.read()
    sock.send(data)
    print 'File received'

def receive_file(sock):
    #Function to receive file

    data = sock.recv(size)
    user_input = raw_input(data)
    sock.send(user_input)
    data = sock.recv(40960)
    if user_input.endswith('.txt'):
        file = open('file.txt','w')
   
    elif user_input.endswith('.pdf'):
        file=open('file.pdf','w')
    
    elif user_input.endswith('.png'):
        file=open('file.png','w')
    
    file.write(str(data))
    file.close()
    print 'File sent'


def listen_client(user_input):
    # It listens to other clients who wants to connect.
    
    listen_port = int(user_input)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Make new socket to able to listen to other client.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host,listen_port))

    print 'Listening'
    sock.listen(backlog)
    client_list = [sock]
    
    while True:
        #Select will take client_list and see if any I/O operations has taken place and wait.
        #Insocks = sockets from which we expect to read
        #Outsocks = sockets to which we write
        #Errsocks = sockets that may have error
        
        Insocks, Outsocks, Errsocks = select.select(client_list,[],[])
        for s in Insocks:
            if sock == s:
                client, address = sock.accept()
                client_list.append(client)
                print 'connected'
                client.send('Start typing')

            else:
                try:
                    data = s.recv(size)
                    if data:
                        if data != 'send_file':
                            print 'Freind-->', data
                        
                        if data == 'send_file':
                            print 'File incoming\n'
                            send_file(client)

                        if data == 'close':
                            print 'session ended'
                            client.close()
                            break

                        user_input = raw_input('Me --> ')
                        client.send(user_input)
                        if user_input == 'send_file':
                            receive_file(client)    

                        if user_input == 'close ':
                            print 'Session ended'
                            client.close()
                            break
                except:
                    client.close()
                    input.remove(client)
                    
    return             


def connect_client(data):
    # Connect to listening client and data is the port of the listening client               

    client_port = int(data)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Make a new port to bind to the listening client
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        soc.connect((host,client_port))
    except:
        print 'Unable to connect to client'

    print 'You are now connected to ' 
    
    while True:
        data = soc.recv(size)
        if data != 'send_file':
            if data == 'Start typing':
                print data

            else:    
                print 'Freind-->', data
        
        if data == 'send_file':
            send_file(soc)

        if data == 'close':
            print 'Session ended. Bye!!'
            soc.close()
            break

        user_input = raw_input('Me --> ')
        soc.send(user_input)
        if user_input == 'send_file':
            receive_file(soc)  

        if user_input == 'close':
            print 'Session ended'
            soc.close()
            break

    return

def client():
    #Make connection to server 

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Creating a socket.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Same as in server. Make socket to be usable by many others.

    try:
        sock.connect((host,port)) # Connect to the server

    except:
        print 'Unable to connect to chat server'
        sys.exit()

    while True:
        data = sock.recv(size)
        if data.isdigit() and int(data) > 2000:  # Checks if the data send is the port number of a client
            connect_client(data)
        
        user_input = raw_input(data)
        sock.send(user_input)
        if user_input.isdigit() and int(user_input)>2000: # Checks if port is given by user than it is a listener
            listen_client(user_input)

        if user_input == 'D' or user_input == 'd':
            sock.close()
            break

if __name__ == '__main__':
    sys.exit(client())