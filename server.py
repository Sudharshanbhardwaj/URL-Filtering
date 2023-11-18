import argparse
import socket
import sys
from _thread import *

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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', listening_port))
        sock.listen(max_connection)
        print("[*] Server started successfully [ %d ]" %(listening_port))
    except Exception as e:
        print("[*] Unable to Initialize Socket")
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = sock.accept() #Accept connection from client browser
            data = conn.recv(buff_size) #Recieve client data
            start_new_thread(conn_string, (conn,data, addr)) #Starting a thread
        except KeyboardInterrupt:
            sock.close()
            print("\n[*] Graceful Shutdown")
            sys.exit(1)
    sock.close()

def conn_string(conn, data, addr):
    try:
        #print(data)
        first_line = data.split(b'\n')[0]

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
        #print(data)
        print(webserver)
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
            proxy_server(webserver, port, conn, addr, data)
        else:
            print("Error 404")
            conn.sendall("HTTP/1.1 404 page not found\r\n\r\n".encode())
        #proxy_server(webserver, port, conn, addr, data)
    except Exception:
        pass

def proxy_server(webserver, port, conn, addr, data):
    try:
        #print(data)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webserver, port))
        sock.send(data)

        while 1:
            reply = sock.recv(buff_size)
            if(len(reply)>0):
                conn.send(reply)
                
                dar = float(len(reply))
                dar = float(dar/1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))

            else:
                break

        sock.close()

        conn.close()
    except socket.error:
        sock.close()
        conn.close()
        print(sock.error)
        sys.exit(1)



if __name__== "__main__":
    start()