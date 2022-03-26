import socket
import sys
from _thread import *

nodes = {
    'node1' : ('127.0.0.1', 8001), #8 letras (a-h)
    'node2' : ('127.0.0.1', 8000), #9 letras (i-q)
    'node3' : ('127.0.0.1', 8003)  #9 letras (r-z)
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
            host_node, port = chooseNode(dataClientArray[1])
            sendToNode(dataClient, host_node, port)

#Método que convierte la clave enviada por el cliente a número segun ASCII
def convertToAscii(letter):

    num = ord(letter)
    return num

#Método que elige a que nodo enviar la información según la clave
def chooseNode(key):

    newKey = convertToAscii(key)

    if newKey >= 97 and newKey <= 104: #8 letras (a-h)
        return nodes['node1']
    elif newKey >= 105 and newKey <= 113: #9 letras (i-q)
        return nodes['node2']
    elif newKey >= 114 and newKey <= 122: #9 letras (r-z)
        return nodes['node3']
    else:
        return nodes['node3']

#Método que envía la información del cliente al nodo y luego del servidor al cliente
def sendToNode(data, host_node, port):

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