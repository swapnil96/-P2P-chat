#!/usr/bin/python

import socket
import os
import sys
import select
import thread

host = '0.0.0.0'
port = 10101
backlog = 10
size = 4096

def instruction(client):
    # Give details of the instructions

    msg = "'H/h' to see the commands for any requests. \n'L/l' For list of the active clients. \n'C/c' For connecting to your friend using username of friend. \n'D/d' To disconnect.\n"
    client.send(msg)

def register(client, credentials, username, password, client_info):
    # Register new users

    if credentials.has_key(username):
        client.send('Person with same Username is already registered. Type "Y" to set new Username\n')
    
    else:
        credentials[username] = password
        mood(client,client_info,username)
        client.send('Type your request or type "H" for help' + '\n')

def verify(client, credentials, username, password, client_info):
    # Verify if username and password is present in already present

    if credentials.has_key(username) and credentials[username] == password:
        client.send('Welcome back ' +username + '\n')
        mood(client,client_info,username)
        return True
    
    else:
        client.send('Incorrect username or password! Try again' + '\n')
        return False 

def mood(client, client_info, username):
    # Sees if the client wants to connect or wait for connection.

    client.send('Type any key to connect to existing members or "L/l" to wait for someone to connect: ')
    response = client.recv(size)
    if response == 'l' or response == "L":
        client.send('Enter your listening port any number between (2001, 65000)(Except-10101): ')
        responseport = client.recv(size)
        client_info[username] = responseport

def connect(client, client_info):
    # Connects for messaging

    client.send('Username to whom you want to connect: ')
    username = client.recv(size)
    if client_info.has_key(username):
        client.send(client_info[username])
        log[username]
    else:
        client.send('Incorrect Username\n')

def start(client, client_list, credentials, client_info, log):
    # Main function. Its starts when a initial data is send by the client

    try:
        data = client.recv(size)

        if data == 'y' or data == 'Y':    # Asks for new username and password to new users.
            client.send('Set new Username & Password:' + '\n' + 'Username: ')
            username = client.recv(size)
            client.send('Password: ')
            password = client.recv(size)
            register(client,credentials,username,password,client_info)
        
        elif data == 'n' or data == 'N':   # If existing user, it verifies the username and password.
            for x in xrange(3):          #Provides 3 attempts to user for login.
                client.send('Type your Username and Password\nUsername: ')
                username = client.recv(size)
                client.send('Password: ')
                password = client.recv(size)
                if verify(client,credentials,username,password,client_info) == True:
                    client.send('\n' + 'Type your request or type "H" for help - ' )
                    break

                if x == 2:
                    client.send('You have exceeded the no. of attempts. For security reasons we cannot log you in now. Come back again!!')        
        

        if data == 'h' or data == 'H': #If help is asked
            instruction(client)    

        if data == 'l' or data == 'L': #Send list of clients to server
            client.send('List: ' +str(credentials.keys()) + '\n')

        if data =='c' or data == 'c':       #Connect the said username for chatting
            connect(client,client_info) 

        if data == 'D' or data == 'd':    #Disconnect client if requested
            client.close()
            client_list.remove(client)

        else:
           pass

    except:
        client.close()
        client_list.remove(client)   
        
#main to create initial connection
def server():
    #creating a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Specifies that the rules used in validating addresses supplied to bind() should allow reuse of local addresses.
    #the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #binding the socket to localhost and port
    sock.bind((host,port))
    
    #Backlog is 10. It is queue of client before server accpets a client. After that free slot is made in queue.
    sock.listen(backlog)

    client_list = [sock] #Stores the list of all active clients.
    credentials = {}    #Store username and password.
    client_info = {}  #Stores username and port numbers.
    log = {}     #to store chat sessions
    print "Chat server is now running on port " + str(port)
    while True:
        #Select will take client_list and see if any I/O operations has taken place and wait.
        #Insocks = sockets from which we expect to read
        #Outsocks = sockets to which we write
        #Errsocks = sockets that may have error
        Insocks, Outsocks, Errsocks = select.select(client_list,[],[])
        for s in Insocks:
            
            if s == sock: #Check is s is the Server sock. It means that a new connection can be made if someone wants to.
                client, address = sock.accept()
                print >>sys.stderr, 'New connection from', address
                client_list.append(client)
                client.send('Welcome to Talkies.' + '\n' + 'Chat with friends in the network and share files too.' + '\n' +'Register today.' + '\n')
                client.send('If you are a new user type Y else N: ')
            
            else:
                start(s, client_list, credentials, client_info, log) #Start getting messages and preferances of clients

if __name__ == '__main__':
    server()