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
        self.canvas.grid(column=0, row=0,columnspan=6,rowspan=3)
        self.canvas2 = tkinter.Canvas(self.window, width=640, height=360)
        self.window.grid_columnconfigure(6, minsize=100)  # Here

        self.canvas2.grid(column=7, row=0,columnspan=6,rowspan=3)
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
        colorCalibrar.set("rojo") # default value

        w = OptionMenu(self.window, colorCalibrar, 'blanco','rojo','verde','azul','amarillo','naranja')
        w.grid(column=1, row=4,sticky="ew")
    
        texto=Canvas(self.window, width=400, height=50)
        texto.grid(column=7, row=5 ,columnspan=6)
        texto.create_text(200,25,fill="darkblue",font="Times 20 italic bold",text='Calibración Actual HSV:')
        texto2=Canvas(self.window, width=400, height=50)
        texto2.grid(column=1, row=5 ,columnspan=6)
        texto2.create_text(200,25,fill="darkblue",font="Times 20 italic bold",text='Calibración Actual RGB:')

        colores=['blanco','rojo','verde','azul','amarillo','naranja']
        canvases = list()
        columna=7
        row=6
        for index,color in enumerate(colores):
            if(columna==10):
                row=row+1
                columna=7
            canvases.append(Canvas(self.window, width=100, height=100))
            canvases[index].grid(column=columna, row=row ,columnspan=1)
            canvases[index].create_text(50,50,fill="darkblue",font="Times 20 italic bold",
                        text=color)
            canvases[index].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.calibracionHSV[color][0]/179, self.videoObject.calibracionHSV[color][1]/255, self.videoObject.calibracionHSV[color][2]/255)))
            columna=columna+1

        columna=1
        row=6
        for index,color in enumerate(colores):
            index=index+6
            if(columna==4):
                row=row+1
                columna=1
            canvases.append(Canvas(self.window, width=100, height=100))
            canvases[index].grid(column=columna, row=row ,columnspan=1)
            canvases[index].create_text(50,50,fill="darkblue",font="Times 20 italic bold",
                        text=color)
            canvases[index].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in (self.videoObject.calibracionRGB[color][0]/255, self.videoObject.calibracionRGB[color][1]/255, self.videoObject.calibracionRGB[color][2]/255)))
            columna=columna+1


        def calibrate():
            #print(messagebox.askyesno(message="¿Desea calibrar el color "+str(colorCalibrar.get())+' a el tono del cuadrado central?', title="Título"))
            print(colorCalibrar.get())
            print(self.videoObject.centroRGB)
            #self.videoObject.calibrate(colorCalibrar.get(), self.datosFrame)
            #print(tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.centro[0]/179, self.videoObject.centro[1]/255, self.videoObject.centro[2]/255)))
            self.videoObject.calibracionHSV[colorCalibrar.get()]=[self.videoObject.centroHSV[0], self.videoObject.centroHSV[1], self.videoObject.centroHSV[2]]
            self.videoObject.calibracionRGB[colorCalibrar.get()]=[self.videoObject.centroRGB[0], self.videoObject.centroRGB[1], self.videoObject.centroRGB[2]]

            canvases[colores.index(colorCalibrar.get())].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.calibracionHSV[colorCalibrar.get()][0]/179,self.videoObject.calibracionHSV[colorCalibrar.get()][1]/255,self.videoObject.calibracionHSV[colorCalibrar.get()][2]/255)))
            canvases[colores.index(colorCalibrar.get())+6].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in (self.videoObject.calibracionRGB[colorCalibrar.get()][0]/255,self.videoObject.calibracionRGB[colorCalibrar.get()][1]/255,self.videoObject.calibracionRGB[colorCalibrar.get()][2]/255)))

        
        btn2 = Button(self.window, text="Calibrar", command=calibrate, fg="black", bg="white")
        btn2.configure(bg='#33cc33')
        btn2.grid(column=2, row=4)







wi= Window()
