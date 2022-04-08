import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import threading
import tkinter
from tkinter import filedialog as fd
from PIL import ImageTk, Image 
import base64

response = []
servidor = []
fileTypes = (('All files', '*.*'),('text files', '*.txt'))

def comprobar(ip,port):
    try:
        port = int(port)
        socket.inet_pton(socket.AF_INET,ip)
        if 1 <= port <= 65535:
            servidor.append(ip)
            servidor.append(port)
            print(tuple(servidor))
            return ip,port
        else:
            raise Exception('This is NOT a VALID port number')
    except Exception as e:
        messagebox.showerror(e, 'Error: Los datos ingresados no son correctos')
        return None

def conectar(nodo = None):
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if nodo:
            mySocket.connect(nodo)
            return mySocket
        mySocket.connect(tuple(servidor))
        return mySocket
    except Exception as e:
        response.append(0)
        messagebox.showerror('Error connection',f'Error: {e}')


def recibir(mySocket):
    res=b''
    header1 = mySocket.recv(30)
    length = int(header1.decode().strip())
    while len(res)<length:
        dat = mySocket.recv(4096)
        if not dat:
            break
        res+=dat
    return res

def enviar(mySocket,msg):
    try:
        msg = msg.encode()
        header = f"{len(msg):<{30}}".encode()
        mySocket.send(header+msg)
        res = recibir(mySocket)
        response.append(res.decode())
    except Exception as e:
        response.append(0)
        messagebox.showerror('Error sending data',f'Error: {e}')
    mySocket.close()

class VentanaEmergente(tk.Toplevel):
    def __init__(self, *args, operation=None,filename=None,nodo=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(width=400, height=300)
        self.resizable(False, False)
        self.focus()
        self.grab_set()

        self.operation = operation
        self.filename = filename

        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.pack(side="top", fill="x", pady=20)
        self.progressbar.start(6)

        msg = f'{operation}||{filename[0]}||{filename}'
        if operation == 5:
            mySocket = conectar(nodo)
        else:
            mySocket = conectar()
        t = threading.Thread(target=enviar, args=[mySocket,msg])
        t.start()

        self.schedule_check(t)
        
    def schedule_check(self,t):
        self.after(1000, self.check_if_done, t)

    def check_if_done(self,t):
        if not t.is_alive():
            self.progressbar.destroy()
            err = response.pop()
            if  err != 0:
                res = err.split('||')
                if self.operation == 5:
                    file = fd.asksaveasfile(title='Guardar archivo como',filetypes = fileTypes, defaultextension = fileTypes,initialfile=self.filename)
                    with open(file.name, "wb") as f:
                        f.write(base64.b64decode(res[2]))
                self.label = ttk.Label(self,text=res[1]).pack(side="top", fill="x", pady=20)
                ttk.Button(self,text="Ok",command=lambda:self.destroy()).pack(side="top", fill="x", pady=20)
        else:
            self.schedule_check(t)
    
class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(width=450, height=600)
        self.resizable(False, False)
        self.title("Base de datos piola")
        self.iconbitmap("Kirb.ico")

        self.etiquetaServer = ttk.Label(self,text="Ingresa la ip del servidor")
        self.etiquetaServer.pack(side="left", fill="x", pady=20)

        self.entradaServer = ttk.Entry(self,foreground = 'grey')
        self.entradaServer.insert(0, '18.211.25.73')
        self.entradaServer.bind('<FocusIn>', self.on_entry_click)
        self.entradaServer.pack(side="left", fill="x", pady=20)

        image = Image.open("image.jpg")
        imageResize = image.resize((250, 250))
        test = ImageTk.PhotoImage(imageResize)

        label = tkinter.Label(image=test)
        label.image = test

        label.pack(side="right")

        self.etiquetaPuerto = ttk.Label(self,text="Ingresa el puerto del servidor")
        self.etiquetaPuerto.pack(side="left", fill="x", pady=20)

        self.entradaPuerto = ttk.Entry(self, foreground = 'grey')
        self.entradaPuerto.insert(0, '8000')
        self.entradaPuerto.bind('<FocusIn>', self.on_entry_click)
        self.entradaPuerto.pack(side="left", pady=20)

        self.ingresar = ttk.Button(self,text="Ingresar",command=self.parametros)
        self.ingresar.pack(side="bottom", fill="x", pady=20)

    def parametros(self):
        datos = comprobar(self.entradaServer.get(),self.entradaPuerto.get())
        if datos:
            self.etiquetaServer.pack_forget()
            self.entradaServer.pack_forget()
            self.etiquetaPuerto.pack_forget()
            self.entradaPuerto.pack_forget()
            self.ingresar.pack_forget()
            self.activarMenu()

    def on_entry_click(self,event):
        if self.entradaPuerto.get() == '8000' and self.entradaServer.get() == '18.211.25.73':
            self.entradaPuerto.delete(0, "end")
            self.entradaPuerto.insert(0, '')
            self.entradaPuerto.config(foreground = 'black')
            self.entradaServer.delete(0, "end")
            self.entradaServer.insert(0, '')
            self.entradaServer.config(foreground = 'black')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def activarMenu(self):
        container = ttk.Frame(self)
        container.pack()

        self.frames = {}

        for F in (Menu, Guardar, VerArchivos, Actualizar):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Menu")

class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="¿Qué operación desea realizar?").pack(side="top", pady=20, anchor=tkinter.CENTER)

        ttk.Button(self, text="Guardar",
                    command=lambda: controller.show_frame("Guardar")).pack(pady=5)
        ttk.Button(self, text="Ver archivos",
                    command=lambda: controller.show_frame("VerArchivos")).pack(pady=5)
        ttk.Button(self, text="Actualizar",
                    command=lambda: controller.show_frame("Actualizar")).pack(pady=5)

class Guardar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = ttk.Label(self, text="Guardar")
        self.label.pack(side="top", pady=10,anchor=tkinter.CENTER)

        self.respuesta = ttk.Label(self, text="")
        self.respuesta.pack(side="top", pady=10,anchor=tkinter.CENTER)
        
        self.botonArchivo = ttk.Button(self, text="Abrir archivo",
                           command=self.abrirArchivo )

        self.botonArchivo.pack(side="top", pady=20)
        self.button = ttk.Button(self, text="Regresar",
                           command=self.ocultarBotones)
        self.button.pack(side="bottom")

    def ocultarBotones(self):
        self.respuesta.config(text='')
        self.controller.show_frame("Menu")

    def abrirArchivo(self):
        self.file = fd.askopenfile(mode='rb',title='Abrir archivo',initialdir='./',filetypes=fileTypes)
        if not self.file: return
        filename = self.file.name.rsplit('/',maxsplit=1)[1]
        key = filename[0]
        data = base64.b64encode(self.file.read()).decode('ascii')
        self.file.close()
        msg = '1||' + key + '||' + filename + '||' + data
        self.enviarMSG(msg)

    def enviarMSG(self, msg):

        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.pack(side="top", pady=20)
        self.progressbar.start(6)

        self.botonArchivo.config(state="disabled")
        self.button.config(state="disabled")
        mySocket = conectar()
        t = threading.Thread(target=enviar, args=[mySocket,msg])
        t.start()

        self.schedule_check(t)
        
    def schedule_check(self,t):
        self.after(1000, self.check_if_done, t)
        
    def check_if_done(self,t):
        if not t.is_alive():
            self.progressbar.destroy()
            err = response.pop()
            self.botonArchivo.config(state="normal")
            self.button.config(state="normal")
            if  err != 0:
                self.respuesta.config(text= err)
            else:
                self.respuesta.config(text= '')
        else:
            self.schedule_check(t)
                
class VerArchivos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = ttk.Label(self, text="Ver archivos")
        self.label.pack(side="top", pady=10, anchor=tkinter.CENTER)

        self.entradaKey = ttk.Entry(self)
        self.entradaKey.pack(side="top", pady=15,anchor=tkinter.CENTER)
        
        self.respuesta = tk.Listbox(self)
        self.respuesta.pack(side="top", pady=10)

        self.buttonframe = tk.Frame(self)

        tk.Button(self.buttonframe, text = "Eliminar",command=self.eliminarDatos).grid(row=0, column=0,padx=5)
        tk.Button(self.buttonframe, text = "Actualizar",command=lambda: controller.show_frame("Actualizar")).grid(row=0, column=1,padx=3)
        tk.Button(self.buttonframe, text = "Descargar",command=self.descargarDatos).grid(row=0, column=2,padx=5)

        self.botonArchivo = ttk.Button(self, text="Buscar",
                           command=self.enviarMSG)
        self.botonArchivo.pack(side="top", pady=20)

        self.button = ttk.Button(self, text="Regresar",
                           command= self.ocultarBotones)
        self.button.pack(side="bottom")

    def ocultarBotones(self):
        self.buttonframe.pack_forget()
        self.respuesta.delete(0,tkinter.END)
        self.controller.show_frame("Menu")

    def enviarMSG(self):

        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.pack(side="top", pady=20)
        self.progressbar.start(6)

        self.entradaKey.config(state=tkinter.DISABLED)
        self.button.config(state="disabled")
        self.botonArchivo.config(state="disabled")
    
        msg = '2||' + self.entradaKey.get()
        mySocket = conectar()
        t = threading.Thread(target=enviar, args=[mySocket,msg])
        t.start()

        self.schedule_check(t)
        
    def schedule_check(self,t):
        self.after(1000, self.check_if_done, t)
        
    def check_if_done(self,t):
        if not t.is_alive():
            self.progressbar.destroy()
            self.entradaKey.config(state=tkinter.NORMAL)
            self.button.config(state="normal")
            self.botonArchivo.config(state="normal")
            err = response.pop()
            if  err != 0:
                res = err.split('||')
                try:
                    self.nodo = (res[0],int(res[1]))
                    msg = '2||' + self.entradaKey.get()
                    mySocket = conectar(self.nodo)
                    header = f"{len(msg):<{30}}".encode()
                    mySocket.send(header+msg.encode())
                    recibido = recibir(mySocket).decode()
                    mySocket.close()
                    self.respuesta.delete(0,tkinter.END)
                    valores = recibido.split(':',maxsplit=1)
                    key,data = valores[0],valores[1].split('/')
                    for i,index in enumerate(data,1):
                        self.respuesta.insert(i,index)
                    self.buttonframe.pack(side="top", pady=10,before=self.botonArchivo)
                except Exception as e:
                    response.append(0)
                    messagebox.showerror('Error lectura',f'Error: {e}')
        else:
            self.schedule_check(t)

    def descargarDatos(self):
        VentanaEmergente(operation=5,filename = self.respuesta.get(self.respuesta.curselection()),nodo=self.nodo)
        self.respuesta.delete(0,tkinter.END)
    
    def eliminarDatos(self):
        VentanaEmergente(operation=3,filename = self.respuesta.get(self.respuesta.curselection()))
        self.respuesta.delete(0,tkinter.END)

class Actualizar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Actualizar")
        label.pack(side="top", pady=10 ,anchor=tkinter.CENTER)

        label = ttk.Label(self, text="Escriba el nombre del archivo que desea actualizar (ej: color.txt):")
        label.pack(side="top", pady=10 ,anchor=tkinter.CENTER)

        self.entradaKey = ttk.Entry(self)
        self.entradaKey.pack(side="top", pady=15,anchor=tkinter.CENTER)

        self.botonArchivo = ttk.Button(self, text="Cargar archivo nuevo",
                           command=self.abrirArchivo )
        self.botonArchivo.pack(side="top", pady=20)

        self.boton = ttk.Button(self, text="Actualizar",
                           command=self.enviarMSG)

        self.boton.pack(side="top", pady=20)

        self.respuesta = ttk.Label(self, text="")
        self.respuesta.pack(side="top", pady=10,anchor=tkinter.CENTER)

        button = ttk.Button(self, text="Regresar",
                           command=self.ocultarBotones)
        button.pack()

    def ocultarBotones(self):
        self.respuesta.config(text='')
        self.controller.show_frame("Menu")

    def enviarMSG(self):

        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.pack(side="top", pady=2)
        self.progressbar.start(6)

        self.entradaKey.config(state=tkinter.DISABLED)
        self.boton.config(state="disabled")
        self.botonArchivo.config(state="disabled")
        mySocket = conectar()
        t = threading.Thread(target=enviar, args=[mySocket,self.msg])
        t.start()

        self.schedule_check(t)
        
    def schedule_check(self,t):
        self.after(1000, self.check_if_done, t)
        
    def check_if_done(self,t):
        if not t.is_alive():
            self.progressbar.destroy()
            self.entradaKey.config(state=tkinter.NORMAL)
            self.boton.config(state="normal")
            self.botonArchivo.config(state="normal")
            err = response.pop()
            if  err != 0:
                self.respuesta.config(text=err)
        else:
            self.schedule_check(t)

    def abrirArchivo(self):
        self.file = fd.askopenfile(mode='rb',title='Abrir archivo',initialdir='./',filetypes=fileTypes)
        if not self.file: return 
        filename = self.file.name.rsplit('/',maxsplit=1)[1]
        key = filename[0]
        data = base64.b64encode(self.file.read()).decode('ascii')
        self.file.close()
        self.msg = '4||' + key + '||' + self.entradaKey.get() + '||' + data

root = VentanaPrincipal()
root.mainloop()