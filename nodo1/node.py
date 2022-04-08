import json
import socket
import sys
import os
from _thread import *

def createRequest(data):
    header = f"{len(data):<{30}}".encode()
    return header+data

#Método que recibe los datos del servidor y ejecuta la lógica del nodo
def node(client:socket.socket):

    global dataClients

    dataClients = json.loads(getFile("dataclients.json"))
    header = client.recv(30).decode().strip()
    length = int(header[0])
    datos = b''
    while len(datos)<length:
        try:
            dataServer = client.recv(4096)
            if not dataServer:
                break
            datos += dataServer
        except:
            break
    
    operations(datos.decode())
        

#Método que ejecuta las operaciones solicitadas por el cliente
def operations(dataServer):

    dataServerArray = dataServer.split('||')
    msg=b''
    if dataServerArray[0] == '1':
        if os.path.exists(dataServerArray[2]):
            msg = 'El archivo ' + dataServerArray[1] + ' ya existe. Pruebe de nuevo!'
        else:
            with open(dataServerArray[2], "w") as file:
                file.write(dataServerArray[3])
            save(dataServerArray[1], dataServerArray[2])
            print(' [x] Se guardó el archivo: ', dataServerArray[2])
            msg = 'El archivo ' + dataServerArray[2] + ' se guardó correctamente!'

    elif dataServerArray[0] == '2':
        print(' [x] Enviando los datos de la clave: ' + dataServerArray[1])
        msg = get(dataServerArray[1])

    elif dataServerArray[0] == '3':
        print(' [x] Archivo a eliminar: ', dataServerArray[2])
        filename =  dataServerArray[2]
        os.remove(filename)
        print(' [x] Archivo ' + dataServerArray[2] + ' eliminado!')
        msg = delete(dataServerArray[1], dataServerArray[2])

    elif dataServerArray[0] == '4':
        print(' [x] Archivo a actualizar: ', dataServerArray[2])
        filename =  dataServerArray[2]

        with open( dataServerArray[2], "w") as file:
            file.write(dataServerArray[3])

        msg = update(dataServerArray[1], dataServerArray[2], dataServerArray[3])

    elif dataServerArray[0] == '5':
        print(' [x] Archivo a descargar: ', dataServerArray[2])
        filename = dataServerArray[2]

        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = file.read()
            msg = '1||Se descargó el archivo: ' + dataServerArray[2] + '||' + data 
        else:
            msg = '0||El archivo ' + dataServerArray[2] + ' no existe!'

    response = createRequest(msg.encode())
    conn.send(response)

#Método que obtiene toda la información del json para poder ser modificada
def getFile(filename):
    try:
        file  = open(filename, "r")
        data = file.read()
        file.close()
        return data
    except FileNotFoundError:
        print("file {filename} does not exist")
        raise

#Método que guarda las modificaciones en el json
def saveFile(filename, data):

    file = open(filename, "w")
    json.dump(data, file)
    file.close()

#Método que guarda información en el json
def save(key, filename):
    print("LA KEY ES ", key)
    print("FILENAME", filename)
    if key in dataClients.keys():
        dataClients[key].append(filename)
    else:
        dataClients[key] = []
        dataClients[key].append(filename)
    saveFile("dataclients.json", dataClients)

#Método que obtiene los valores de una llave de acuerdo al json
def get(key):

    if key in dataClients.keys():
        msg = key + ':' + '/'.join(dataClients[key])
    else:
        msg = 'Error:La clave del archivo no fue encontrada!'
    return msg

#Método que elimina la información del json
def delete(key, filename):

    if key in dataClients.keys():
        dataClients[key] = [dato for dato in dataClients[key] if dato != filename]
        saveFile("dataclients.json", dataClients)
        msg = '1||El archivo ' + filename + ' se eliminó correctamente!'
    else:
        msg = '0||El archivo ' + filename + ' no existe!'
    return msg

#Método que actualiza la información en el json
def update(key, filename, value):
    msg = 'El archivo ' + filename + ' no existe!'
    if key in dataClients.keys():
        for n in dataClients[key]:
            if n == filename:
                delete(key, filename)
                save(key, filename, value)
                msg = 'El archivo se ' + filename + ' actualizó correctamente!'
                break
    return msg


#Método que identifica los parámetros al ejecutar la aplicación
def parameters():

    if len(sys.argv) == 2:
        port = sys.argv[1]
        print(' [x] Port:', port)
        
    else:
        port = '8000'
        print(' [x] Se estableción el puerto', port, 'por defecto. Si desea usar otro puerto cierre la aplicación y recuerde ingresar:')
        print(' [x] Recuerder ingresar: $python3 node.py <port>')
        print(' [x] Ejemplo: $python3 node.py', port)
        
    return port

def mostrar(port):
    nodeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nodeSock.connect(('127.0.0.1',8000))
    nodeSock.setblocking(False)
    message = f'Reveal||{port}'
    request = createRequest(message.encode())
    nodeSock.send(request)

if __name__ == '__main__':
    try:
        if not os.path.exists('dataclients.json'):
            with open('dataclients.json','w') as file:
                file.write('{}')
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        port = int(parameters())
        mostrar(port)
        mySocket.bind( (host, port) ) 
        mySocket.listen(5) 

        print('------ Runnning Node Application ------')
        
        while True:
            conn, addr = mySocket.accept()
            print(" [x] Conexión desde: " + str(addr))
            start_new_thread(node, (conn, ))

    except Exception as error:
        print(socket.error)