import time
import SocketServer
# Protocol
# NAME ""
# SAY ""
# LEAVE
# 
# Chatroom
# room = {name1 : socket1,
#         name2 : socket2,
#         .
#         .
#         .
#         }



class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.name = ''
        while True:
            input_message = self.rfile.readline()
            print "Input message was {}".format(input_message)
            if input_message.startswith("NAME"):
                name_componets = input_message.strip().split()[1:]
                self.name = " ".join(name_componets)
                self.server.room[self.name] = self.wfile
                print "{} has joined the room".format(self.name)
            elif input_message.startswith("SAY"):
                message_to_send = input_message.replace("SAY ","{} says".format(self.name))
                for user in self.server.room:
                    if user != self.name:
                        print "  Sending message to {}".format(user)
                        user_connection = self.server.room[user]
                        user_connection.write(message_to_send)
            elif input_message.startswith("LEAVE"):
                self.wfile.write("Goodbye {}!".format(self.name))
                del self.server.room[self.name]
                break
            else:
                self.wfile.write("Bad message")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    def __init__(self, *largs, **kargs):
        self.room = {}
        SocketServer.TCPServer.__init__(self, *largs, **kargs)

server = ThreadedTCPServer(("localhost", 9999), Handler)
server.serve_forever()
