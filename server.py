import socket
import sys
from _thread import *

nodes = []

letrasAscii = list(range(33,127))

def splitArray(a, n):
    k, m = divmod(len(a), n)
    return list(a[i*k + min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def createRequest(data):
    header = f"{len(data):<{30}}".encode()
    return header+data

#Método que recibe los datos del cliente y ejecuta la lógica del servidor
def server(client):
    message_header = client.recv(30)
    message_length = int(message_header.decode().strip())
    datos = b''
    while len(datos)<message_length:
        try:
            dataClient = client.recv(1024)
            if not dataClient:
                break
            datos += dataClient
        except:
            raise
    dataClientArray = datos.decode().split('||')
    if dataClientArray[0] == 'Reveal':
        nodes.append(('127.0.0.1',int(dataClientArray[1])))
        return
    elif  dataClientArray[0] == '2':
        host_node, port =  chooseNode(dataClientArray[1])
        print(' [x] Enviando al cliente nodo solicitado: ',host_node, port)
        datos = createRequest(f'{host_node}||{port}'.encode())
        conn.send(datos)
    else:
        print("SOY EL DATA CLIENT", dataClientArray[:-1])
        enviado = False
        while not enviado:
            host_node, port =  chooseNode(dataClientArray[1])
            enviado = sendToNode(datos, host_node, port)

#Método que convierte la clave enviada por el cliente a número segun ASCII
def convertToAscii(letter):
    num = ord(letter)
    return num

#Método que elige a que nodo enviar la información según la clave
def chooseNode(key):

    newKey = convertToAscii(key)
    if len(nodes) > 1:
        particion = splitArray(letrasAscii,len(nodes))
        for index,letras in enumerate(particion):
            if newKey in letras:
                return nodes[index]
    else:
        return nodes[0]

#Método que envía la información del cliente al nodo y luego del servidor al cliente
def sendToNode(data, host_node, port):
    print("SOY EL HOST NODE ",(host_node))
    print("SOY EL PORT NODE ",(port))
    try: 
        nodeSocket = socket.socket()
        nodeSocket.connect( (host_node, port) )
    except:
        nodes.remove((host_node, port))
        return False
    peticion = createRequest(data)
    nodeSocket.sendall(peticion)
    message_header = nodeSocket.recv(30)
    message_length = int(message_header.decode().strip())
    datos = b''
    while len(datos)<message_length:
        try:
            dataClient = nodeSocket.recv(1024)
            if not dataClient:
                break
            datos += dataClient
        except:
            raise
    respuesta = createRequest(datos)
    conn.send(respuesta)
    nodeSocket.close()
    
    return True

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
            print(" [x] Conexión desde: ", str(addr))
            start_new_thread(server, (conn,))

    except Exception as error:
        print(socket.error)