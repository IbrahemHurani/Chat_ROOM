import tkinter as tk
import socket
import threading


window = tk.Tk()
window.title("Server")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
Welocome=tk.Label(topFrame,text="Welcome to my project Chat Room server").pack()
btnStart = tk.Button(topFrame, text="Connect Server", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop Server", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))





# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: 0.0.0.0")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:0000")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="Client List:").pack(side=tk.LEFT)
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=20, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="blue", highlightbackground="gray", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))






server = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []

bottomFrame = tk.Frame(window)
msg=tk.Label(bottomFrame,text="Write  message !").pack(side=tk.LEFT)
tkMessage = tk.Text(bottomFrame, height=2, width=50)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
#getChatMessage(tkMessage.get("1.0", tk.END)
tkMessage.bind("<Return>", (lambda event:getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


# Start server function
def start_server():
    global client2,server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server With TCP Running .....!")
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(100)  # server is listening for client connection
    tkMessage.config(state=tk.NORMAL)
    threading._start_new_thread(accept_clients, (server, " "))


    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    global client2
    while True:
        client, addr = the_server.accept()
        client2=client
        clients.append(client)
        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "

    # send welcome message to client
    client_name  = client_connection.recv(4096).decode()
    welcome_msg = "Welcome to my Chat Room " + client_name + ". Use 'exit' to quit"
    client_connection.send(welcome_msg.encode())

    clients_names.append(client_name)

    update_client_names_display(clients_names)  # update client names display


    while True:
        data = client_connection.recv(4096).decode()
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "GOOD BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    index = 0
    for c in client_list:
        if c == curr_client:
            break
        index = index + 1

    return index


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


def getChatMessage(msg):
    global client2
    msg_server=str(msg)
    welcome_msg = "server :" + msg_server+" "
    for c in clients:
        c.send(welcome_msg.encode())



window.mainloop()