import socket
import threading

import Tkinter

# read_message is a simple function that runs in a separate thread.
# It will keep reading messages from the server and dropping them in
# the messages window
def read_messages(sock, messages):
    while True:
        # The following lines will read the data and put it on the
        # screen with a newline. The hardcoded 100 is a bad idea. We
        # should really have a message delimiter or some kind of
        # format that tells us the size upfront.
        data = sock.recv(100)
        messages.insert(Tkinter.END, data+'\n')
        # This will scroll the window till the end so that as messages
        # come, the text window will scroll down.
        messages.see(Tkinter.END)

# The following two lines setup our connection to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 9999))

# We send our name at the beginning. Ideally, the GUI would prompt us
# to enter a name at first and then use that. We hardcode this due to 
# lack of time.
sock.send("NAME Noufal\n")

# Create the root window. This is the main window inside which
# everything else is there.
root = Tkinter.Tk()

# This is a Text widget. Used to print multiple lines of
# text http://effbot.org/tkinterbook/text.htm
server_messages = Tkinter.Text()
# This is a Frame widget. Used to pack multiple widgets for alignment
# purposes. In our case, we want the entry widget and send button to
# be in one line so we put it in a frame.
# http://effbot.org/tkinterbook/frame.htm
input_frame = Tkinter.Frame()
# We create an Entry widget http://effbot.org/tkinterbook/entry.htm
# that can receive one line of text.
my_input = Tkinter.Entry(input_frame)

# This is the callback for the button which will do 4 things. This
# function will get called when the "Send!" button is pushed. It will
# 1. Read out the message from the "my_input" entry widget.
# 2. Prepend "SAY" to the message and add a newline at the end.
# 3. Send it to the server
# 4. Clear the entry widget.
def send_message():
    message_to_be_sent = my_input.get()
    sock.send("SAY {}\n".format(message_to_be_sent))
    my_input.delete(0, Tkinter.END)
              
# This creates the send button. Not the "input_frame" as the first
# parameter which tells it that it should be a child of the frame
# rather than the root window (as in the case of the server_messages
# widget).
send_button = Tkinter.Button(input_frame, text="Send!", command = send_message)

# pack the widgets. For the meanings of the parameters, refer to
# http://effbot.org/tkinterbook/
send_button.pack(side = Tkinter.RIGHT, fill = Tkinter.X)
my_input.pack(side = Tkinter.RIGHT, fill = Tkinter.X, expand=True)
server_messages.pack(side = Tkinter.TOP, fill = Tkinter.X)
input_frame.pack(side = Tkinter.TOP, fill = Tkinter.X)

# Create and start a thread to update the messages window in the background.
update_thread = threading.Thread(target=read_messages, args = [sock, server_messages])
update_thread.start()

# Start the gui
root.mainloop()

