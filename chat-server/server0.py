#!/usr/bin/env python
"""
A very simple TCP server in Python. 

The lines have been commented for your reference. 

"""


# Imports the modules that we need to get this working.
import time
import socket # This is the abstraction for the network interfaces

# Creates a socket that can be connected to by a remote machine.  Type
# "man 7 socket" in the terminal for the meanings of AF_INET,
# SOCK_STREAM etc.  This is a very low level interface and not the way
# people mostly write socket servers in Python. However, it will allow
# us to see the primitives so that we know what we're doing. 
# This is much more like programming in C than in Python.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This will free the bound port (9999) when the program
# terminates. Otherwise, we have to wait a long time before we can
# restart it.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# "Bind"s the socket to the host,port pair mentioned. This advertises
# to the world that our chat server is available on this machine at
# port 9999. That's the "address" which clients should "connect" to.
sock.bind(("localhost", 9999))
# This will make the socket wait for connections. Connections are
# received using the "accept" call below.
sock.listen(0)

print "Server started..."

# An infinite loop that will serve one connection at a time.
while True:
    # The program will block here till someone tries to connect.  When
    # that happens, sock.accept will return a pair of objects. A new
    # socket which can be used to communicate with the remote client
    # and a number specifying the connection.
    client_sock, address = sock.accept()
    print "Connection from {}".format(address)
    # The following loop is the "work" done by our server. It simply
    # sends 5 messages to the client with 1 second intervals between
    # them.
    for i in range(5):
        time.sleep(1)
        client_sock.send("Hello "+str(i)+"\n")
    print "  - Done"
    # Closes the client socket thus ending the connection.
    client_sock.close()



    


