# -P2P-chat
Peer to Peer chatting and file sending using a central server as a connector.

Application description

SERVER
1) The server uses socket.setsockopt to reuse the socket many times. Basically it waits for another requests.
2) SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
3) It then queues 10(backlog) clients before server accpets a client. After that free slot is made in queue.
4) Then the server for any connections from client using select feature of select module.
5) Whenever a new connection is created it prompts the client asking either it wants to listen or connect to someone.
6) If a connection can be made then it connects the 2 clients and its role is over. So even if the server is disconnected the clients can 		continue to connect as their connecting by themselves.
7) The cleint that was waiting to be connected acts as the server for the session.

CLIENT
1) It has 2 options to select. Either it can connect to existing clients or wait someone to connect to it.
2) When it waits to be connected by someone it basically acts as server listening other clients who want to connect to it.
3) After connection it can send messages or send files ('.txt', '.png', and '.pdf'). Other format of files can also be sent by modifying the 	code.


Instructions to USE

1) Extract the server and client python files.
2) Run the chatserver.py file in the terminal.
3) You need to change the IP address of host in chatclient.py file according to the IP of the host machine.
4) Now open a new terminal and run chatclient.py file.
5) The server will ask if you are a new client or a registered client. Type 'Y' or 'N'.
5) You will be asked to set a new username and password or type your existing username and password.
6) If the new username you are trying to set already exists, then you will be asked to set a new username by typing 'Y'.
7) After you set your username you will be asked to set up your listening port, where other client can connect.
8) If you are existing user and provide incorrect username for 3 consecutive attempts, you will be blocked.
9) After this initial log in, you can type your command to be sent to server or type 'h/H' to get command list.
10) From the help list you can type 'L/l' to get list of clients and 'C/c' to connect other client by typing the username that will be 			displayed. Basically in this step you are getting the port number of the other client and connecting to it.
11) Your window will display if you are connected to the user and then you can chat or send file.
12) You can send files to other clients during chat by typing 'send_file' command which will also be available in the help list.
13) To end chat session, send 'close' command and your will be disconnected.
14) Type (Ctrl+C) command in server terminal to disconnect.