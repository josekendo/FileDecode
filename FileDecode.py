#!/usr/bin/env python
# coding: utf8
# -*- coding: utf-8 -*-

#Este software es de uso personal, no da ninguna garantia
#Podras descifrar tus archivos con tecnica de descompresion y descifrado salsa20 e cast


import tkinter as tk
from tkinter import filedialog,simpledialog,messagebox
import easygui
from PIL import ImageTk, Image
import Crypto 
from Crypto.Cipher import Salsa20,CAST
from Crypto.Hash import SHA256
import pickle
import os
import base64
import zipfile

def label(apli,tex):
    return tk.Label(apli,text=tex)

def entry(apli):
    return tk.Entry(apli)

def button(apli,tex):
    return tk.Button(apli,text=tex)

def descomprimir():
    #recogemos la variable global
    global archivoTemp
    global archivo
    pathname = os.path.dirname(archivo)
    #nombre temporal 
    comprimido = "tempComprimido.zip"
    archivoTemp = comprimido
    #generamos una instancia para extraer el archivo comprimido
    ziper = zipfile.ZipFile(comprimido)
    ziper.extractall(pathname)
    ziper.close()

def borrarComprimido():
    #asi se llamara el archivo temporal
    global archivoTemp
    #borramos el archivo temporal
    os.remove(archivoTemp)

def encode():
    comprobar()

def estadoBotonDecodificando():
    global app
    boton2Text.set("Decodificando...")
    boton2.place(x=30,y=110)
    boton2.config(bg="orange")

def estadoBotonDecodificado():
    boton2Text.set("Decodificado")
    boton2.place(x=33,y=110)
    boton2.config(bg="green")
    messagebox.showinfo(title="Decodificado correcto",message="Su archivo ha sido decodificado ;)")

def estadoBotonError():
    boton2Text.set("Decodificar")
    boton2.place(x=38,y=110)
    boton2.config(bg="blue")
    messagebox.showerror(title="Decodificacion Erronea",message="Ocurrio un error al intentar decodificar el archivo, su contraseña puede ser erronea o el archivo estar defectuoso :( ")

def comprobar():
    global campo, archivo
    if(len(campo.get()) < 6):
        messagebox.showwarning(title="El password es demasiado pequeño",message="Por favor, ponga un password de minimo 6 digitos.")
    elif(archivo == ''):
        messagebox.showwarning(title="No hay archivo seleccionado",message="Por favor, seleccione un archivo a decodificar.")
    else:
        estadoBotonDecodificando()
        encriptar(1)
        

def openfile():
  global archivo
  global boton
  archivo =  tk.filedialog.askopenfilename()
  if(archivo != '' and len(archivo) > 0):
    boton.config(bg="green",fg="white",command=openfile)
  else:
    boton.config(bg="white",fg="black",command=openfile)

def encriptar(version):
    #encriptamos con distintos algoritmos
    global archivo
    global campo
    if(version == 1):
        try:
            secret = encriptarPass(campo.get())
            msg = base64.b64decode(open(archivo,'rb').read())#se decodea al binario original
            msg_nonce = msg[:8] #primer byte es un registro
            cipherfile = msg[8:] #resto de los datos
            cipher = Salsa20.new(key=secret,nonce=msg_nonce)
            cifrado = cipher.decrypt(cipherfile)
            guardado = open("tempComprimido.zip","wb")
            guardado.write(cifrado)
            guardado.close()
            descomprimir()
            borrarComprimido()
            estadoBotonDecodificado()
        except:
            estadoBotonError()

def encriptarNombre(path):
    global campo
    filename = os.path.basename(path)
    pathname = os.path.dirname(path)
    key = encriptarPassH(campo.get())
    msg = bytes(base64.b64decode(filename.replace("-@-","/")))
    eiv = msg[:CAST.block_size+2]
    ciphertext = msg[CAST.block_size+2:]
    cipher = CAST.new(bytes(key[0:16],"utf-8"), CAST.MODE_OPENPGP, eiv)
    nombreoriginal = str(cipher.decrypt(ciphertext),"utf-8")
    return pathname+"/"+nombreoriginal

def encriptarPass(valor):
    cipher = SHA256.new(data=bytes(valor,'utf-8'))
    return cipher.digest()

def encriptarPassH(valor):
    cipher = SHA256.new(data=bytes(valor,'utf-8'))
    return cipher.hexdigest()

archivo = ''
archivoTemp = ''
app = tk.Tk()
scwidth = app.winfo_screenwidth()
scheight = app.winfo_screenheight()
xcoor = int((scwidth/2) - (290/2))
ycoor = int((scheight/2.4) - (150/2))
app.title("FileDecode KJ v1.Temis")
app.config(bg="black")
app.resizable(False, False)
app.geometry("290x150+{}+{}".format(xcoor, ycoor))
app.iconbitmap(sys._MEIPASS+"\img\decode.ico")

image = Image.open(sys._MEIPASS+"\img\karen.png")
image = image.resize((100, 150), Image.ANTIALIAS) 
img = ImageTk.PhotoImage(image)
imglabel = tk.Label(app, image=img)    
imglabel.config(bg="black")
imglabel.place(x=80,y=0,relwidth=1, relheight=1)

#canvas = tk.Canvas(app, bg="black", width=100, height=150)
#canvas.pack()

titulo = label(app,"FileDecode KJ")
titulo.config(justify="left",bg="black",fg="white",font=("Verdana",14))
titulo.pack()
titulo.place(x=0,y=0)

etiqueta = label(app,"Password:")
etiqueta.config(justify="left",bg="black",fg="white",font=("Verdana",12))
etiqueta.pack()
etiqueta.place(x=8,y=30)

campo = entry(app)
campo.config(bg="black",fg="white",justify="center",show="*")
campo.pack()
campo.place(x=10,y=52)

boton = button(app,"Abrir fichero")
boton.config(bg="white",fg="black",command=openfile)
boton.pack()
boton.place(x=35,y=76)

boton2 = button(app,"Decodificar")
boton2Text = tk.StringVar()
boton2.config(bg="blue",fg="white",textvariable=boton2Text,command=encode)
boton2Text.set("Decodificar")
boton2.pack()
boton2.place(x=38,y=110)

app.mainloop()



