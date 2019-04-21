from tkinter import *
import cv2
import PIL.Image
import PIL.ImageTk
import tkinter
import Video as videoImport
import time
import threading
from tkinter import messagebox
import colorsys
import numpy as np

class Window:
    
    def refresh(self):
        #imagen = cv2.imread("../../Recursos/cara1.png")
        #imagen = cv2.resize(imagen, (192, 108))
        #photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imagen))
        #return photo

        #RGB / RGB2
        frame,frame2,cara=self.videoObject.getFrame()

        if(cara!=None):
            carasOrdenadasporX=sorted(cara, key=lambda x: x[2], reverse=True)
            abajo=sorted([carasOrdenadasporX[0],carasOrdenadasporX[1],carasOrdenadasporX[2]], key=lambda x: x[1], reverse=False)
            medio=sorted([carasOrdenadasporX[3],carasOrdenadasporX[4],carasOrdenadasporX[5]], key=lambda x: x[1], reverse=False)
            arriba=sorted([carasOrdenadasporX[6],carasOrdenadasporX[7],carasOrdenadasporX[8]], key=lambda x: x[1], reverse=False)
            print(abajo)
            print(medio)
            print(arriba)
            image=np.zeros((300, 300, 3), np.uint8)
            for index,color in enumerate(arriba):
                image[0:100,(index+1)*100-100:(index+1)*100] = color[3] 
            for index,color in enumerate(medio):
                image[100:200,(index+1)*100-100:(index+1)*100] = color[3] 
            for index,color in enumerate(abajo):
                image[200:300,(index+1)*100-100:(index+1)*100] = color[3] 
            image[99:100,:] = [0,0,0]
            image[199:200,:] = [0,0,0]
            image[:,99:100] = [0,0,0]
            image[:,199:200] = [0,0,0]

            cv2.namedWindow("ResultadosCara", 1)
            def ResultadosCara(event,x,y,flags,param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    print(x,y)
            cv2.setMouseCallback('ResultadosCara',ResultadosCara)
            cv2.imshow( "ResultadosCara", image ); 

        '''
            result=messagebox.askyesno("Guardar Cara","¿Quieres Guardar los datos?")
            print(result)
            if result == True:
                print("Guardado Cubo!")
                cv2.imshow( "Cara Guardada", image ); 
        '''

        self.datosFrame=frame

        self.frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.frame, anchor=tkinter.NW)
        
        self.frame2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
        self.canvas2.create_image(0, 0, image=self.frame2, anchor=tkinter.NW)
        return frame


    def __init__(self):
        self.videoObject= videoImport.Video.inicializaVideo()
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


        def cambioModo():
            if switch.config('text')[-1] == 'Normal':
                switch.config(text='Espectacular')
                self.videoObject.modo='Espectacular'
            else:
                switch.config(text='Normal')
                self.videoObject.modo='Normal'


        switch =  Button(self.window,text="Normal", width=12, command=cambioModo)
        switch.grid(column=6, row=1 ,columnspan=1)
     
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
            #print(self.videoObject.calibracionAuto[colorCalibrar.get()]) no ira con el rojo
            #print(messagebox.askyesno(message="¿Desea calibrar el color "+str(colorCalibrar.get())+' a el tono del cuadrado central?', title="Título"))
            print(colorCalibrar.get())
            #self.videoObject.calibrate(colorCalibrar.get(), self.datosFrame)
            #print(tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.centro[0]/179, self.videoObject.centro[1]/255, self.videoObject.centro[2]/255)))
            self.videoObject.calibracionHSV[colorCalibrar.get()]=[self.videoObject.centroHSV[0], self.videoObject.centroHSV[1], self.videoObject.centroHSV[2]]
            self.videoObject.calibracionRGB[colorCalibrar.get()]=[self.videoObject.centroRGB[0], self.videoObject.centroRGB[1], self.videoObject.centroRGB[2]]
            canvases[colores.index(colorCalibrar.get())].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(self.videoObject.calibracionHSV[colorCalibrar.get()][0]/179,self.videoObject.calibracionHSV[colorCalibrar.get()][1]/255,self.videoObject.calibracionHSV[colorCalibrar.get()][2]/255)))
            canvases[colores.index(colorCalibrar.get())+6].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in (self.videoObject.calibracionRGB[colorCalibrar.get()][0]/255,self.videoObject.calibracionRGB[colorCalibrar.get()][1]/255,self.videoObject.calibracionRGB[colorCalibrar.get()][2]/255)))
            #calibracion modo auto
            refPt = [(260, 118), (360, 217)]
            roi = self.datosFrame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            hsvRoi = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
            if(colorCalibrar.get()!='rojo' and colorCalibrar.get()!='blanco'):
                #con buena iluminacion
                '''
                self.videoObject.calibracionAuto[colorCalibrar.get()][0] = np.array([np.percentile(hsvRoi[:,:,0],15), np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                self.videoObject.calibracionAuto[colorCalibrar.get()][1] = np.array([np.percentile(hsvRoi[:,:,0],85), np.percentile(hsvRoi[:,:,1],85), np.percentile(hsvRoi[:,:,2],85)],np.uint8)
                '''
                #con mala iluminacion
                print(np.percentile(hsvRoi[:,:,0],10),np.percentile(hsvRoi[:,:,0],90))
                self.videoObject.calibracionAuto[colorCalibrar.get()][0] = np.array([np.percentile(hsvRoi[:,:,0],15), np.percentile(hsvRoi[:,:,1],5), np.percentile(hsvRoi[:,:,2],5)])
                self.videoObject.calibracionAuto[colorCalibrar.get()][1] = np.array([np.percentile(hsvRoi[:,:,0],85), 255, 255])
            elif(colorCalibrar.get()=='blanco'):
                self.videoObject.calibracionAuto[colorCalibrar.get()][0] = np.array([np.percentile(rectHSV[:,:,0],15), 0, np.percentile(rectHSV[:,:,2],20)])
                self.videoObject.calibracionAuto[colorCalibrar.get()][1] = np.array([np.percentile(rectHSV[:,:,0],85), np.percentile(rectHSV[:,:,1],95), 255])
            else:
                hueMax=np.percentile(hsvRoi[:,:,0],85)
                hueMin=np.percentile(hsvRoi[:,:,0],15)
                #caso 170-180 0-10
                if hueMin<60 and hueMax>50:
                    self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMax, np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                    self.videoObject.calibracionAuto['rojo1'][1] = np.array([180, 255, 255],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][0] = np.array([0, np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMin, 255, 255],np.uint8)
                #caso 150-179 o # 0-10
                else:
                    self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMin, np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                    self.videoObject.calibracionAuto['rojo1'][1] = np.array([hueMax, 255, 255],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][0] = np.array([hueMin, np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMax, 255, 255],np.uint8)



        btn2 = Button(self.window, text="Calibrar", command=calibrate, fg="black", bg="white")

        btn2.configure(bg='#33cc33')
        btn2.grid(column=2, row=4)

        self.x_start=0
        self.y_start=0
        self.x_end=0
        self.y_end=0
        self.cropping=False
        self.getROI=False

        def calibrateClick():
            def showPixelValue(event,x,y,flags,param):
                imagenbgr= cv2.cvtColor(self.datosFrame, cv2.COLOR_RGB2BGR)
                imagenrgb= self.datosFrame
                imagenHSV= cv2.cvtColor(self.datosFrame, cv2.COLOR_RGB2HSV)

                if event == cv2.EVENT_LBUTTONDOWN:
                    self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
                    self.cropping = True
                elif event == cv2.EVENT_MOUSEMOVE:
                    if self.cropping == True:
                        self.x_end, self.y_end = x, y
                elif event == cv2.EVENT_LBUTTONUP:
                    # record the ending (x, y) coordinates and indicate that
                    # the cropping operation is finished
                    self.x_end, self.y_end = x, y
                    self.cropping = False
                    self.getROI = True
                    #calibramos con la media 
                    #Ordenamos los puntos por orden, xddd
                    yArriba=max(self.y_start,self.y_end)
                    yAbajo=min(self.y_start,self.y_end)
                    xIzquierda=min(self.x_start,self.x_end)
                    xDerecha=max(self.x_start,self.x_end)
                    height, width, channels = imagenrgb.shape
                    #print(height, width, channels)
                    #rectangulos cortados
                    rectRgb = imagenrgb[yAbajo:yArriba,xIzquierda:xDerecha]
                    rectHSV = imagenHSV[yAbajo:yArriba,xIzquierda:xDerecha]
                    #cv2.imshow("croped",rectRgb)
                    mediaRGB=cv2.mean(rectRgb)
                    mediaHSV=cv2.mean(rectHSV)
                    #self.videoObject.calibracionHSV[colorCalibrar.get()]=[colorsys.rgb_to_hsv(media[0],media[1],media[2])]
                    self.videoObject.calibracionRGB[colorCalibrar.get()]=[mediaRGB[0], mediaRGB[1], mediaRGB[2]]
                    canvases[colores.index(colorCalibrar.get())+6].configure(bg= '#%02x%02x%02x' % (round(mediaRGB[0]), round(mediaRGB[1]), round(mediaRGB[2])))
                    self.videoObject.calibracionHSV[colorCalibrar.get()]=[mediaHSV[0], mediaHSV[1], mediaHSV[2]]
                    canvases[colores.index(colorCalibrar.get())].configure(bg= '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(mediaHSV[0]/179,mediaHSV[1]/255,mediaHSV[2]/255)))
                    #calibracion auto
                    if(colorCalibrar.get()!='rojo' and colorCalibrar.get()!='blanco' ):
                        #con buena iluminacion
                        '''
                        self.videoObject.calibracionAuto[colorCalibrar.get()][0] = np.array([np.percentile(rectHSV[:,:,0],15), np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                        self.videoObject.calibracionAuto[colorCalibrar.get()][1] = np.array([np.percentile(rectHSV[:,:,0],85), np.percentile(rectHSV[:,:,1],85), np.percentile(rectHSV[:,:,2],85)],np.uint8)
                        '''
                        #con mala iluminacion
                        print(np.percentile(rectHSV[:,:,0],10),np.percentile(rectHSV[:,:,0],90))
                        self.videoObject.calibracionAuto[colorCalibrar.get()][0] = np.array([np.percentile(rectHSV[:,:,0],15), np.percentile(rectHSV[:,:,1],5), np.percentile(rectHSV[:,:,2],5)])
                        self.videoObject.calibracionAuto[colorCalibrar.get()][1] = np.array([np.percentile(rectHSV[:,:,0],85), 255, 255])
                    #el rojo no vale solo ponerle el minimo y el maximo ya que suele empezar por 170 y acabar por 10
                    elif(colorCalibrar.get()=='blanco'):
                        self.videoObject.calibracionAuto[colorCalibrar.get()][0] = np.array([np.percentile(rectHSV[:,:,0],15), 0, np.percentile(rectHSV[:,:,2],20)])
                        self.videoObject.calibracionAuto[colorCalibrar.get()][1] = np.array([np.percentile(rectHSV[:,:,0],85), np.percentile(rectHSV[:,:,1],95), 255])
                    else:
                        hueMax=np.percentile(rectHSV[:,:,0],85)
                        hueMin=np.percentile(rectHSV[:,:,0],15)
                        #caso 170-180 0-10
                        if hueMin<60 and hueMax>50:
                            self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMax, np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                            self.videoObject.calibracionAuto['rojo1'][1] = np.array([180, 255,255],np.uint8)
                            self.videoObject.calibracionAuto['rojo2'][0] = np.array([0, np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                            self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMin, 255,255],np.uint8)
                        #caso 150-179 o # 0-10
                        else:
                            self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMin, np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                            self.videoObject.calibracionAuto['rojo1'][1] = np.array([hueMax, 255,255],np.uint8)
                            self.videoObject.calibracionAuto['rojo2'][0] = np.array([hueMin, np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                            self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMax, 255,255],np.uint8)

                # get the value of pixel from the location of mouse in (x,y)
                bgr = imagenbgr[y,x]

                # Convert the BGR pixel into other colro formats
                hsv = cv2.cvtColor(np.uint8([[bgr]]),cv2.COLOR_BGR2HSV)[0][0]
                rgb = cv2.cvtColor(np.uint8([[bgr]]),cv2.COLOR_BGR2RGB)[0][0]

                # Create an empty placeholder for displaying the values
                placeholder = np.zeros((imagenbgr.shape[0],400,3),dtype=np.uint8)

                # fill the placeholder with the values of color spaces
                cv2.putText(placeholder, "HSV {}".format(hsv), (20, 140), cv2.FONT_HERSHEY_COMPLEX, .9, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(placeholder, "RGB {}".format(rgb), (20, 70), cv2.FONT_HERSHEY_COMPLEX, .9, (255,255,255), 1, cv2.LINE_AA)

                # Combine the two results to show side by side in a single image
                combinedResult = np.hstack([imagenrgb,placeholder])
                if self.cropping and not self.getROI:
                    cv2.rectangle(combinedResult, (self.x_start, self.y_start), (self.x_end, self.y_end), (0, 255, 0), 2)

                elif not self.cropping and self.getROI:
                    cv2.rectangle(combinedResult, (self.x_start, self.y_start), (self.x_end, self.y_end), (0, 255, 0), 2)
                
                combinedResult= cv2.cvtColor(combinedResult, cv2.COLOR_RGB2BGR)
                self.i=combinedResult
                cv2.namedWindow("Calibracion")
                cv2.imshow('Calibracion',self.i)

            if(not hasattr(self, 'i')):
                self.i=  self.datosFrame.copy()
            cv2.namedWindow("Calibracion")
            cv2.imshow('Calibracion',self.i)
            cv2.setMouseCallback('Calibracion',showPixelValue)

        btn3 = Button(self.window, text="Calibrar con click", command=calibrateClick, fg="black", bg="white")

        btn3.configure(bg='#33cc33')
        btn3.grid(column=3, row=4)








wi= Window()
