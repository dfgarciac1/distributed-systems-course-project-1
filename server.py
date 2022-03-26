import socket
import sys
from _thread import *
import os
import subprocess
    
os.environ['NODE1_HOST'] = '127.0.0.1'
os.environ['NODE2_HOST'] = '127.0.0.1'
os.environ['NODE3_HOST'] = '127.0.0.1'
os.environ['NODE1_PORT'] = "8001"
os.environ['NODE2_PORT'] = "8002"
os.environ['NODE3_PORT'] = "8003"


nodes = {
 
}

#Método que recibe los datos del cliente y ejecuta la lógica del servidor
def server(client):

    while True:

        try:
            dataClient = client.recv(1024).decode()
        except error:
            print('Error de lectura.')
            break
        
        if len(dataClient):
            dataClientArray = dataClient.split('||')
            print("SOY EL DATA CLIENT", dataClientArray)
            host_node, port =  chooseNode(dataClientArray[1])
            sendToNode(dataClient, host_node, port)

#Método que convierte la clave enviada por el cliente a número segun ASCII
def convertToAscii(letter):

    num = ord(letter)
    return num

#Método que elige a que nodo enviar la información según la clave
def chooseNode(key):

    newKey = convertToAscii(key)
    nodeSocket = socket.socket()

    if newKey >= 97 and newKey <= 104: #8 letras (a-h)
        if 'node1' in nodes:
            return nodes['node1']
        else:
            try:
             nodeSocket.connect( (os.environ.get("NODE1_HOST"),  int(os.getenv("NODE1_PORT"),)))
            except:
                subprocess.call("node.py "+ os.getenv("NODE1_PORT"), shell=True)
                print("")
            nodes['node1'] = (os.environ.get("NODE1_HOST"), int(os.getenv("NODE1_PORT")))
        return nodes['node1']
    elif newKey >= 105 and newKey <= 113: #9 letras (i-q)
        if 'node2' in nodes:
            return nodes['node2']
        else:
            try:
             nodeSocket.connect( (os.environ.get("NODE2_HOST"),  int(os.getenv("NODE2_PORT"),)))
            except:
                subprocess.call("node.py "+ os.getenv("NODE2_PORT"), shell=True)
                print("EJECUTE EN 2 ")
            nodes['node2'] = (os.environ.get("NODE2_HOST"), int(os.getenv("NODE2_PORT")))       
            return nodes['node2']
    elif newKey >= 114 and newKey <= 122: #9 letras (r-z)
        if 'node3' in nodes:
            return nodes['node3']
        else:
            try:
             nodeSocket.connect( (os.environ.get("NODE3_HOST"),  int(os.getenv("NODE3_PORT"),)))
            except:
                subprocess.call("node.py "+ os.getenv("NODE3_PORT"), shell=True)
            nodes['node3'] = (os.environ.get("NODE3_HOST"), int(os.getenv("NODE3_PORT")))       
            return nodes['node3']
    else:
        return nodes['node3']

#Método que envía la información del cliente al nodo y luego del servidor al cliente
def sendToNode(data, host_node, port):
    print("SOY EL HOST NODE ",(host_node))
    print("SOY EL PORT NODE ",(port))
    nodeSocket = socket.socket()
    nodeSocket.connect( (host_node, port) )
    nodeSocket.send(data.encode())
    dataNode = nodeSocket.recv(1024).decode()
    print(' [x] Enviando: ' + dataNode)
    conn.send(dataNode.encode())
    nodeSocket.close()

#Método que identifica los parámetros al ejecutar la aplicación
def parameters():

    if len(sys.argv) == 2:
        port = sys.argv[1]
        print(' [x] Port:', port)
        
    else:
        port = '8000'
        print(' [x] Se estableción el puerto', port, 'por defecto. Si desea usar otro puerto cierre la aplicación y recuerde ingresar:')
        print(' [x] Recuerder ingresar: $python3 server.py <port>')
        print(' [x] Ejemplo: $python3 server.py', port)
        
    return port

if __name__ == '__main__':
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        port = int(parameters())
        mySocket.bind( (host, port) ) 
        mySocket.listen(5) 

        print('------ Runnning Server Application ------')
        
        while True:
            conn, addr = mySocket.accept()
            print(" [x] Conexión desde: " + str(addr))
            start_new_thread(server, (conn, ))

    except Exception as error:
        print(socket.error)