#!/usr/bin/env python

import time
# This is more Pythonic way of creating TCP/UDP servers
import SocketServer

# This Handler will be what is created everytime someone connects. 
# The handle method will be called and the class will have all the 
# things necessary to commmunicate
class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        # This part is very similar to the the part inside the "While
        # True" in the previous program.
        print self.server.room
        while True:
            message = self.rfile.readline().strip()
            print "We got {}".format(message)
            for i in range(10):
                time.sleep(1)
                # The self.wfile is created by the TCPServer class and has
                # the client_socket which we can write to but wrapped
                # around to look like a regular Python file.
                self.wfile.write("{} {}\n".format(message,i))
            print "  - Done"

# This line creates a TCP Server that can handle multiple connections
# using threads.
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # This will internally do the setsockopt call that we saw in the
    # previous program
    allow_reuse_address = True
    # This overrides the default __init__ function of TCPServer and
    # creates a "room" attribute that we can access inside the
    # handler. This will hold our actual chat room.
    def __init__(self, *largs, **kargs):
        self.room = []
        SocketServer.TCPServer.__init__(self, *largs, **kargs)
        
        
        

server = ThreadedTCPServer(("localhost", 9999), Handler)
server.serve_forever()
