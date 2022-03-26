import socket
import sys

#Método que hace la conexión con el servidor y le pregunta al cliente por las operaciones que desea realizar
def client():

    server, port = parameters()    

    mySocket = socket.socket() #Se llama al método socket
    mySocket.connect( (server, int(port)) )

    print('------ Runnning Client Application ------')
    print(' [x] ¿Qué operación desea realizar? Escriba únicamente el número: ')
    print('      1. Guardar \n      2. Ver archivos \n      3. Eliminar \n      4. Actualizar \n      5. Descargar \n      6. Salir de la aplicación ')
         
    while True:

        operation = input(" >")
        msg = ""
        serverData = ""
        if operation == '1': #PUT
            print(' [x] Escriba el nombre del archivo que desea guardar (ej: color.txt): ')
            filename = input(" >")
            key = filename[0].lower()
            newFilename = filename
            filename = 'client_files/' + filename
            print("FILENAME", filename)
            file = open(filename, "r") # r -> read
            data = file.read()
            file.close()
            msg = operation + '||' + key + '||' + newFilename + '||' + data
            mySocket.send(msg.encode())
            serverData = mySocket.recv(1024).decode()
            print(serverData)          

        elif operation == '2': #GET
            print(' [x] Escriba la clave para ver los archivos disponibles (solo una letra): ')
            key = input(" >")
            msg = operation + '||' + key
            mySocket.send(msg.encode())
            serverData = mySocket.recv(1024).decode()
            print(serverData)

        elif operation == '3': #DELETE
            print(' [x] Escriba el nombre del archivo que desea eliminar (ej: color.txt): ')
            filename = input(" >")
            key = filename[0].lower()
            newFilename = filename
            msg = operation + '||' + key + '||' + newFilename
            mySocket.send(msg.encode())
            serverData = mySocket.recv(1024).decode()
            print(serverData)

        elif operation == '4':
            print(' [x] Escriba el nombre del archivo que desea actualizar (ej: color.txt): ')
            filename = input(" >")
            key = filename[0].lower()
            newFilename = filename
            filename = 'client_files/' + filename 
            file = open(filename, "r") # r -> read
            data = file.read()
            msg = operation + '||' + key + '||' + newFilename + '||' + data
            mySocket.send(msg.encode())
            serverData = mySocket.recv(1024).decode()
            print(serverData)
            file.close()
        
        elif operation == '5':
            print(' [x] Escriba el nombre del archivo que desea descargar (ej: color.txt): ')
            filename = input(" >")
            key = filename[0].lower()
            msg = operation + '||' + key + '||' + filename
            mySocket.send(msg.encode())
            serverData = mySocket.recv(1024).decode()
            dataArray = serverData.split('||')

            if dataArray[0] == '1':
                file = open('client_files/' + filename, "w")# w -> write
                file.write(dataArray[2])
                file.close()
                print(dataArray[1])                
            elif dataArray[0] == '0':
                print(dataArray[1])

        elif operation == '6':
            print(' [x] Hasta luego...')
            break

        else:
            print(' [x] Operación no válida, intente de nuevo:')

        print( '\n [x] ¿Qué operación desea realizar? Escriba únicamente el número: ')
    mySocket.close() #Se termina la conexión con el servidor

#Método que identifica los parámetros al ejecutar la aplicación
def parameters():
    
    if len(sys.argv) == 3:
        server = sys.argv[1]
        port = sys.argv[2]
        print(' [x] Server:', server,'\n [x] Port:', port)
        
    else:
        print(' [x] Recuerde ingresar: $python3 client.py <ip-sever> <port>')
        print(' [x] Ejemplo: $python3 client.py 34.226.36.159 8000\n')

    return server, port

if __name__ == '__main__':
    client()
    