from tkinter import *
import cv2
import PIL.Image
import PIL.ImageTk
import tkinter
import Video as vedo
import time
import threading
from tkinter import messagebox
import colorsys

class Window:

    def refresh(self):
        #imagen = cv2.imread("../../Recursos/cara1.png")
        #imagen = cv2.resize(imagen, (192, 108))
        #photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imagen))
        #return photo

        frame,frame2=self.videoObject.getFrame()
        #frame = cv2.resize(frame, (640, 360))
        self.datosFrame=frame
        self.frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.frame, anchor=tkinter.NW)
        
        self.frame2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
        self.canvas2.create_image(0, 0, image=self.frame2, anchor=tkinter.NW)
        return frame


    def __init__(self):
        self.videoObject= vedo.Video.inicializaVideo()
        self.window = Tk()
        self.canvas = tkinter.Canvas(self.window, width=640, height=360)
        self.canvas.grid(column=0, row=0,columnspan=3,rowspan=3)
        self.canvas2 = tkinter.Canvas(self.window, width=640, height=360)
        self.window.grid_columnconfigure(3, minsize=100)  # Here

        self.canvas2.grid(column=4, row=0,columnspan=3,rowspan=3)
        self.frame=self.refresh()
        
        self.createWindow()

        
        #MAIN LOOP
        while True:
            Window.refresh(self)
            self.window.update_idletasks()
            self.window.update()
        



    def video(self):
        self.canvas2.create_image(0, 0, image=self.datosFrame, anchor=tkinter.NW)



    def createWindow(self):


        self.window.title("Seleciona la cara del cubo")

        self.window.geometry('1920x1080')

        colorCalibrar = StringVar(self.window)
        colorCalibrar.set("red") # default value

        w = OptionMenu(self.window, colorCalibrar, "red", "blue", "green")
        w.grid(column=1, row=4)
    
        color1 = Canvas(self.window, width=100, height=100)
        color1.grid(column=4, row=4 ,columnspan=1)
        color1.create_text(50,50,fill="darkblue",font="Times 20 italic bold",
                        text="Rojo")
        
        

        def calibrate():
            #print(messagebox.askyesno(message="¿Desea calibrar el color "+str(colorCalibrar.get())+' a el tono del cuadrado central?', title="Título"))
            print(self.videoObject.centro)
            #self.videoObject.calibrate(colorCalibrar.get(), self.datosFrame)
            print(tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.centro[0]/179, self.videoObject.centro[1]/255, self.videoObject.centro[2]/255)))
            btn2.configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.centro[0]/179, self.videoObject.centro[1]/255, self.videoObject.centro[2]/255)))
            color1.configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.centro[0]/179, self.videoObject.centro[1]/255, self.videoObject.centro[2]/255)))
        btn2 = Button(self.window, text="Calibrar", command=calibrate, fg="black", bg="white")
        btn2.configure(bg='#ff7700')
        btn2.grid(column=2, row=4)







wi= Window()
