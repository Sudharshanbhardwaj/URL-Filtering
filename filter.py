import sys
from urllib.parse import urlparse
from _thread import *
from socket import *


if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

try:
    listening_port = int(input("[*] Enter listening port number: "))
except KeyboardInterrupt:
    print("\n[*] User has requested an interrupt")
    print("[*] Application Exiting.....")
    sys.exit()

max_connection=20
buff_size=8192

def start():    #Main Program
    try:
        # Create a server socket, bind it to a port and start listening
        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind(('', listening_port))
        serverSock.listen(max_connection)
        print("[*] Server started successfully [ %d ]" %(listening_port))
    except Exception as e:
        print("[*] Unable to Initialize Socket")
        print(e)
        sys.exit(2)

    while True:
        try:
            print('\nReady to serve...')
            clientsock, addr = serverSock.accept() #Accept connection from client browser
            print('Received a connection from:', addr)
            message = clientsock.recv(buff_size) #Recieve client data
            start_new_thread(url_extractor, (clientsock, message, addr)) #Starting a thread
        except KeyboardInterrupt:
            serverSock.close()
            print("\n[*] Error while starting thread")
            sys.exit(1)
    serverSock.close()

def url_extractor(clientsock, message, addr):
    try:
        first_line = message.split(b'\n')[0]

        url = first_line.split()[1]

        http_pos = url.find(b'://') #Finding the position of ://
        if(http_pos==-1):
            temp=url
        else:

            temp = url[(http_pos+3):]
        
        port_pos = temp.find(b':')

        webserver_pos = temp.find(b'/')
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]
        print(webserver)
        blocker(webserver, port, addr, message, clientsock)
    except Exception:
        pass


def blocker(webserver, port, addr, message, clientsock):

    if(port==443): #if the request is of type HTTP(S)
        print("proxy server unable to obtain the certificate to decrpyt TLS/SSL security")
        #thread.exist()
        #thread._Thread_stop()

    blackList = open("blacklist.txt", "r")
    flag = False
    for line in blackList.readlines():
        line = line.split('\n')[0]
        if line == webserver:
            print("This URL is blocked")
            flag = True
            break

    blackList.close()
    
    if flag==False:
        #passing the control to the proxy server to obtain the data from the remote server
        proxy_server(webserver, port, addr, message, clientsock)
    else:
        print("Error 404")
        clientsock.sendall("HTTP/1.1 404 page not found\r\n\r\n".encode())

def proxy_server(webserver, port, addr, message,clientsock):
    rServersock = socket(AF_INET, SOCK_STREAM)
    
    ip_address = socket.gethostbyname(webserver)

    print(ip_address)
    
    try:
        print('Connected to port')
        rServersock.connect((webserver, port))
        rServersock.send(message)  # Send the entire request

        
        while 1:
            reply = rServersock.recv(buff_size)            
            if(len(reply)>0):
                clientsock.send(reply)
                
                dar = float(len(reply))
                dar = float(dar/1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))
            else: 
                break

    except Exception as e:
        print(f"Error: {e}")
        clientsock.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())

    
    rServersock.close()    
    clientsock.close()

if __name__== "_main_":
    start()
