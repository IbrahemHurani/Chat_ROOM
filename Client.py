import tkinter as tk
from tkinter import messagebox
import socket
import threading

window = tk.Tk()
window.title("Client")
username = " "
clients=[]

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)

btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
ButtonClose=tk.Button(topFrame,text="Close",command=lambda :close())
ButtonClose.pack(side=tk.LEFT)


topFrame.pack(side=tk.TOP)


displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="Your Chat Room ! ").pack(side=tk.LEFT)
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=59)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="white", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(window)
msg=tk.Label(bottomFrame,text="Write  message !").pack(side=tk.LEFT)
tkMessage = tk.Text(bottomFrame, height=2, width=50)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))

Download=tk.Button(bottomFrame,text="Download").pack(side=tk.RIGHT)#!!!!!!!!!!!!!!!!!!!!!!!!you need to add the lambda
##########################3

bottomFrame.pack(side=tk.BOTTOM)


def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Enter your name first")
    else:
        username = entName.get()
        connect_to_server(username)


# network client
client = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080


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

        tkDisplay.config(state=tk.NORMAL)
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