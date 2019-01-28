from tkinter import *
import cv2
import PIL.Image
import PIL.ImageTk
import tkinter
import Video as vedo
import time
import threading

class Window:

    def refresh(self):
        #imagen = cv2.imread("../../Recursos/cara1.png")
        #imagen = cv2.resize(imagen, (192, 108))
        #photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imagen))
        #return photo

        frame,arrayElegido=self.videoObject.getFrame(self.arrayElegido)
        #frame = cv2.resize(frame, (640, 360))
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.arrayElegido=arrayElegido
        return frame


    def __init__(self):
        self.arrayElegido=[]
        self.videoObject= vedo.Video.inicializaVideo()
        image=cv2.imread("../Recursos/cara1.png")
        self.window = Tk()
        photo = image
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(photo))
        self.canvas = tkinter.Canvas(self.window, width=640, height=360)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas.grid(column=0, row=3)

        self.frame=self.refresh()
        self.frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
        self.canvas2 = tkinter.Canvas(self.window, width=640, height=360)
        self.canvas2.create_image(0, 0, image=self.frame, anchor=tkinter.NW)
        self.canvas2.grid(column=3, row=3)
        self.createWindow()

        
        #MAIN LOOP
        while True:
            Window.refresh(self)
            self.window.update_idletasks()
            self.window.update()
        



    def video(self):
        self.canvas2.create_image(0, 0, image=self.refresh(), anchor=tkinter.NW)




    def createWindow(self):


        self.window.title("Seleciona la cara del cubo")

        self.window.geometry('1920x1080')



        value=0
        rad1 = Radiobutton(self.window, text='Superior', value=0)
        rad1.select()
        rad2 = Radiobutton(self.window, text='Inferior', value=1)
        rad2.deselect()
        rad3 = Radiobutton(self.window, text='Frontal', value=2)
        rad3.deselect()
        rad4 = Radiobutton(self.window, text='Izquierda', value=3)
        rad4.deselect()
        rad5 = Radiobutton(self.window, text='Derecha', value=4)
        rad5.deselect()
        rad6 = Radiobutton(self.window, text='Trasera', value=5)
        rad6.deselect()


        rad1.grid(column=0, row=5)
        rad2.grid(column=1, row=5)
        rad3.grid(column=2, row=5)
        rad4.grid(column=3, row=5)
        rad5.grid(column=4, row=5)
        rad6.grid(column=5, row=5)

        lbl = Label(self.window, text="Guardar Cara:")

        lbl.grid(column=0, row=6)


        def clicked():
            lbl.configure(text="Cara guardada !!")



        btn = Button(self.window, text="Guardar", command=clicked, fg="black", bg="white")
        btn.grid(column=1, row=4)

    #    btn = Button(self.window, text="Refrescar Captura", command=self.refresh, fg="black", bg="white")
    #    btn.grid(column=1, row=3)




wi= Window()
