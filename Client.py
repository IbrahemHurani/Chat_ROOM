import os
import tkinter as tk
from tkinter import messagebox
import socket
import threading
from os.path import basename
import tkinter.filedialog
import time
window = tk.Tk()
window.config(background="#7FFFD4")
window.title("Client")
username = " "
clients=[]
file=b''

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:",background="#7FFFD4").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.config(background="#F5F5F5")
topFrame.config(background="#7FFFD4")
entName.pack(side=tk.LEFT)

btnConnect = tk.Button(topFrame, text="Connect",background="#CAFF70" ,command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
ButtonClose=tk.Button(topFrame,text="Close",background="#CAFF70" ,command=lambda :close())
ButtonClose.pack(side=tk.LEFT)

topFrame.pack(side=tk.TOP)


displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="Your Chat Room ! ",background="#FF4040").pack(side=tk.LEFT)
displayFrame.config(background="#7FFFD4")
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=59)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F5F5F5", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(window)
msg=tk.Label(bottomFrame,text="Write  message !",background="#7FFFD4").pack(side=tk.LEFT)
bottomFrame.config(background="#7FFFD4")
tkMessage = tk.Text(bottomFrame, height=2, width=50)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)

bottomFrame2=tk.Frame(window)
NameFile=tk.Label(bottomFrame2,text="File Name",background="#7FFFD4").pack(side=tk.LEFT)
bottomFrame2.config(background="#7FFFD4")
pathFile=tk.Text(bottomFrame2,height=1,width=20)
pathFile.pack(side=tk.RIGHT,padx=(5,13),pady=(5,10))
pathFile.config(highlightbackground="grey", state=tk.NORMAL)
Download=tk.Button(bottomFrame2,text="Download",background="#CAFF70" ,command=lambda :OnDownload(file,pathFile.get("1.0",tk.END))).pack(side=tk.RIGHT)#!!!!!!!!!!!!!!!!!!!!!!!!you need to add the lambda
bottomFrame2.pack(side=tk.LEFT)

def OnDownload(file,fileName):

    fullpath = tk.filedialog.asksaveasfilename(initialdir="/", title="Select file", initialfile=fileName)
    f = open(fullpath, 'wb')
    f.write(file)
    d = os.path.getsize(file)
    file = b''
    print(fullpath)

def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Enter your name first")
    else:
        username = entName.get()
        connect_to_server(username)


# network client
client = None
client2=None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080
filename=''
def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        clients.append(name)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode()) # Send name to server after connecting

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")



def receive_message_from_server(sck, m):
    tkDisplay.config(state=tk.NORMAL)
    while True:
        from_server = sck.recv(4096).decode()

        if not from_server: break

            # display message from server on the chat window

            # enable the display area and insert the text and then disable.
            # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, from_server)
        else:
            tkDisplay.insert(tk.END, "\n"+ from_server)

            tkDisplay.config(state=tk.DISABLED)
            #tkDisplay.see(tk.END)

    sck.close()
    window.destroy()


def getChatMessage(msg):

    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_mssage_to_server(msg):
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")

def close():#for close window
    window.destroy()


window.mainloop()
