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
import SolverKociemba as solver

class Window:
    def refresh(self):
        #imagen = cv2.imread("../../Recursos/cara1.png")
        #imagen = cv2.resize(imagen, (192, 108))
        #photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imagen))
        #return photo

        #RGB / RGB2 /modo auto / modo normal
        frame,frame2,cara,self.arrayElegido=self.videoObject.getFrame()

            
        #si se detecta la cara automaticamente o se pulsa el boton salta la funcion de mostrar la cara
        if((cara!=None and not self.mostrandoCara) or self.guardar==True):
            def mostrarCara(abajo,medio,arriba):
                self.mostrandoCara=True

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
                image[:,299:300] = [0,0,0]
                im = PIL.Image.open("./Recursos/BotonGuardarCara.png")
                np_im = np.array(im)
                image= np.vstack([image,np_im])
                window=cv2.namedWindow("ResultadosCara", 1)
                cv2.moveWindow("ResultadosCara", 500,30)
                def ResultadosCara(event,x,y,flags,param):
                    if event == cv2.EVENT_RBUTTONDOWN:
                        #[['blanco',[255,255,255]],['rojo',[0,0,255]],['azul',[255,0,0]],['verde',[0,255,0]],['naranja',[0, 128, 255]],['amarillo',[0,255,255]]]
                        print("Eligiendo Color")
                        im=np.zeros((300, 120, 3), np.uint8)
                        index=0
                        for i in self.arrayPosiblesColores:
                            im[0+index:50+index,:] = i[1]
                            index=index+50

                        self.posColorCambiar=[x,y] #la posicion del color a cambiar
                        cv2.imshow( "Elige color", im )
                        cv2.moveWindow("Elige color", x+500,y+30)

                        def colorElegido(event,x,y,flags,param):
                            if event == cv2.EVENT_LBUTTONDOWN:
                                print("patata")
                                print(x,y)
                                self.indiceRotatorio=int(y/50) #simulamos la funcion que va rotando pero el color elegido sera el nuestro
                                ResultadosCara(1,self.posColorCambiar[0],self.posColorCambiar[1],None,None)
                                cv2.destroyWindow("Elige color")

                        cv2.setMouseCallback('Elige color',colorElegido)



                        

                    if event == cv2.EVENT_LBUTTONDOWN: #modo de cambio con el click izquierdo
                        if(x<100 and y<100):#cambia el color al siguiente que toca en funcion del lugar
                            cv2.destroyWindow("ResultadosCara")
                            arriba[0][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            arriba[0][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<200 and y<100):
                            cv2.destroyWindow("ResultadosCara")
                            arriba[1][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            arriba[1][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<300 and y<100):
                            cv2.destroyWindow("ResultadosCara")
                            arriba[2][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            arriba[2][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<100 and y<200):
                            cv2.destroyWindow("ResultadosCara")
                            medio[0][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            medio[0][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<200 and y<200):
                            cv2.destroyWindow("ResultadosCara")
                            medio[1][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            medio[1][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<300 and y<200):
                            cv2.destroyWindow("ResultadosCara")
                            medio[2][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            medio[2][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<100 and y<300):
                            cv2.destroyWindow("ResultadosCara")
                            abajo[0][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            abajo[0][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<200 and y<300):
                            cv2.destroyWindow("ResultadosCara")
                            abajo[1][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            abajo[1][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<300 and y<300):
                            cv2.destroyWindow("ResultadosCara")
                            abajo[2][0]=self.arrayPosiblesColores[self.indiceRotatorio][0]
                            abajo[2][3] = self.arrayPosiblesColores[self.indiceRotatorio][1]
                            if(self.indiceRotatorio<5):
                                self.indiceRotatorio=self.indiceRotatorio+1
                            else:
                                self.indiceRotatorio=0
                            mostrarCara(abajo,medio,arriba)
                        elif(x<300 and y<350):
                            result=messagebox.askyesno("Guardar Cara","¿Quieres Guardar los datos?")
                            if result == True:
                                print("Guardado Cubo!")
                                if(self.caraElegida.get()=='frontal'):
                                    sitio=[1,1]
                                
                                if(self.caraElegida.get()=='inferior'):
                                    sitio=[1,2]
                                if(self.caraElegida.get()=='izquierda'):
                                    sitio=[0,1]
                                if(self.caraElegida.get()=='derecha'):
                                    sitio=[2,1]
                                if(self.caraElegida.get()=='superior'):
                                    sitio=[1,0]
                                if(self.caraElegida.get()=='trasera'):
                                    sitio=[3,1]
                                #Responsive Generation
                                if(self.scale_factor>1):
                                    cubo=150
                                    casilla=50
                                else:
                                    cubo=120
                                    casilla=40

                                for index,color in enumerate(arriba):   
                                    self.estadoCubo[sitio[1]*cubo:sitio[1]*cubo+casilla,sitio[0]*cubo+(index+1)*casilla-casilla:sitio[0]*cubo+(index+1)*casilla] = [color[3][2],color[3][1],color[3][0]]
                                for index,color in enumerate(medio):
                                    self.estadoCubo[sitio[1]*cubo+casilla:sitio[1]*cubo+casilla*2,sitio[0]*cubo+(index+1)*casilla-casilla:sitio[0]*cubo+(index+1)*casilla] = [color[3][2],color[3][1],color[3][0]]
                                for index,color in enumerate(abajo):
                                    self.estadoCubo[sitio[1]*cubo+2*casilla:sitio[1]*cubo+cubo,sitio[0]*cubo+(index+1)*casilla-casilla:sitio[0]*cubo+(index+1)*casilla] = [color[3][2],color[3][1],color[3][0]]

                                #rallitas para que quede mejor
                                self.estadoCubo[0:cubo*3:casilla,0:cubo*4] = [240,240,240]
                                self.estadoCubo[0:cubo*3,0:cubo*4:casilla] = [240,240,240]

                                self.estadoCubo[cubo+1,0:cubo*4] = [240,240,240]
                                self.estadoCubo[0:cubo*3,cubo+1] = [240,240,240]
                                
                                
                                self.estadoCubo[cubo*2+1,0:cubo*4] = [240,240,240]
                                self.estadoCubo[0:cubo*3,cubo*3+1] = [240,240,240]
                                
                                self.estadoCubo[cubo-1,0:cubo*4] = [240,240,240]
                                self.estadoCubo[0:cubo*3,cubo-1] = [240,240,240]
                                
                                self.estadoCubo[cubo*2-1,0:cubo*4] = [240,240,240]
                                self.estadoCubo[0:cubo*3,cubo*3-1] = [240,240,240]


                                #GuardamosLosDatos
                                index=0
                                self.datosCubo[self.caraElegida.get()]=[]
                                for casilla in arriba+medio+abajo:
                                    self.datosCubo[self.caraElegida.get()].append(casilla[0])
                                    
                                print(self.datosCubo)
                                #El cubo ya se podria resolver aparece el boton
                                if(len(self.datosCubo)==6):
                                    def resolvedor():
                                        res=solver.LlamadaEntrante(self.datosCubo)
                                        print('resuelto')
                                        messagebox.showinfo("Conclusión del solver:", res)

                                    btn4 = Button(self.window, text="RESOLVER CUBO!", command=resolvedor, fg="black", bg="white")
                                    btn4.configure(bg='#A7C3C2')
                                    btn4.grid(column=8, row=4)
                                self.imagenCuboPintada=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.estadoCubo))
                                cv2.destroyWindow("ResultadosCara")

                cv2.setMouseCallback('ResultadosCara',ResultadosCara)
                cv2.imshow( "ResultadosCara", image )
                self.mostrandoCara=False
            if(self.guardar!=True):
                carasOrdenadasporX=sorted(cara, key=lambda x: x[2], reverse=True)
                abajo=sorted([carasOrdenadasporX[0],carasOrdenadasporX[1],carasOrdenadasporX[2]], key=lambda x: x[1], reverse=False)
                medio=sorted([carasOrdenadasporX[3],carasOrdenadasporX[4],carasOrdenadasporX[5]], key=lambda x: x[1], reverse=False)
                arriba=sorted([carasOrdenadasporX[6],carasOrdenadasporX[7],carasOrdenadasporX[8]], key=lambda x: x[1], reverse=False)
            else:
                self.guardar=False
                abajo=self.modoNormal[0]
                medio=self.modoNormal[1]
                arriba=self.modoNormal[2]
            mostrarCara(abajo,medio,arriba)

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

        self.canvas3.create_image(0, 0, image=self.imagenCuboPintada , anchor=tkinter.NW)

        return frame


    def __init__(self):
        self.mostrandoCara=False
        self.guardar=False
        self.videoObject= videoImport.Video.inicializaVideo()
        self.window = Tk()
        anchura = self.window.winfo_screenwidth()
        altura = self.window.winfo_screenheight()
    # Responsive
        porcentajeAnchura = anchura / (1536 / 100)
        porcentajeAltura = altura / (864 / 100)
        self.scale_factor = ((porcentajeAnchura + porcentajeAltura) / 2) / 100
        print(self.scale_factor)
        fontsize = int(14 * self.scale_factor)
        #tamaño minimo fuente
        if(fontsize<12):
            fontsize=12
        self.font=labelfont = ('times', fontsize, 'bold')

        #self.window.config(font=("Courier",  self.fontsize))

        #Responsive

        self.window.tk.call('tk', 'scaling',self.scale_factor)
        self.canvas = tkinter.Canvas(self.window, width=640, height=360)
        self.canvas.grid(column=0, row=0,columnspan=6,rowspan=4)
        self.canvas2 = tkinter.Canvas(self.window, width=640, height=360)
        self.window.grid_columnconfigure(6, minsize=100) 
        self.canvas2.grid(column=7, row=0,columnspan=6,rowspan=4)
        self.indiceRotatorio=0
        #en BGR
        self.arrayPosiblesColores=[['blanco',[255,255,255]],['rojo',[0,0,255]],['azul',[255,0,0]],['verde',[0,255,0]],['naranja',[0, 128, 255]],['amarillo',[0,255,255]]]
        self.canvas3 = tkinter.Canvas(self.window, width=600, height=450)
        self.canvas3.grid(column=7, row=5,columnspan=8,rowspan=8)

       

        #estado del cubo pintado (imagen que se muestra)
        #Responsive 3 tamaños
        if(self.scale_factor>1):
            self.estadoCubo=image=np.zeros((450, 600, 3), np.uint8)
            self.estadoCubo[0:450:150,0:600] = [255,255,255]
            self.estadoCubo[0:450,0:450:150] = [255,255,255]
            self.estadoCubo[0:150,451:600] = [255,255,255]
            self.estadoCubo[301:450,451:600] = [255,255,255]

            self.imagenCuboPintada=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.estadoCubo))
        else:
            self.estadoCubo=image=np.zeros((360, 480, 3), np.uint8)
            #generamos rallas separadoras
            self.estadoCubo[0:360:120,0:480] = [240,240,240]
            self.estadoCubo[0:360,0:480:120] = [240,240,240]
            #Eliminamos sobrantes
            self.estadoCubo[0:120,241:480] = [240,240,240]
            self.estadoCubo[241:360,241:480] = [240,240,240]
            self.estadoCubo[0:120,0:120] = [240,240,240]
            self.estadoCubo[241:360,0:120] = [240,240,240]

            self.imagenCuboPintada=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.estadoCubo))

        #datos del cubo(igual que los pintados pero sin ser imagen si no datos)
        self.datosCubo={}
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


        self.window.title("TFG Rubik Solver Alejandro Monteseirin")
    
        #self.window.attributes("-fullscreen", True)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        print(width,height)

        #self.window.geometry('1920x1080')
        self.window.geometry(str(width)+'x'+str(height))

        colorCalibrar = StringVar(self.window)
        colorCalibrar.set("rojo") # default value

        #reseta los valores del array elegido al cambiar la cara
        def callback(*args):
            print("Reseteando valores arrayElegido porque la cara cambio")
            self.videoObject.arrayElegido=[[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]],[0,0,0,[0,0,0]]]

        self.caraElegida = StringVar(self.window)
        self.caraElegida.trace("w", callback)

        self.caraElegida.set("frontal") # default value

        w = OptionMenu(self.window, colorCalibrar, 'blanco','rojo','verde','azul','amarillo','naranja')
        w.configure(font=self.font)

        w.grid(column=1, row=4,sticky="ew")

        caraG = OptionMenu(self.window, self.caraElegida, 'frontal','izquierda','derecha','superior','inferior','trasera')
        caraG.configure(font=self.font)
        caraG.grid(column=2, row=4,sticky="ew")

        def cambioModo():
            if switch.config('text')[-1] == 'Normal':
                switch.config(text='Automático')
                self.videoObject.modo='Espectacular'
                self.btn4.destroy()
            else:
                switch.config(text='Normal')
                self.videoObject.modo='Normal'
                self.btn4 = Button(self.window, text="Guardar", command=guardar,font=self.font, fg="black", bg="white")
                self.btn4.configure(bg='#9FE1DE')
                self.btn4.grid(column=6, row=3)


        switch =  Button(self.window,text="Auto",font=self.font, width=12, command=cambioModo)
        switch.grid(column=6, row=1 ,columnspan=1)
     
        texto=Canvas(self.window, width=400, height=50)
        texto.grid(column=1, row=9 ,columnspan=4)
        texto.create_text(150,25,fill="darkblue",font="Times 20 italic bold",text='Calibración Actual HSV:')
        texto2=Canvas(self.window, width=400, height=50)
        texto2.grid(column=1, row=5 ,columnspan=4)
        texto2.create_text(150,25,fill="darkblue",font="Times 20 italic bold",text='Calibración Actual RGB:')

        colores=['blanco','rojo','verde','azul','amarillo','naranja']
        canvases = list()
        columna=1
        row=10
        for index,color in enumerate(colores):
            if(columna==4):
                row=row+1
                columna=1
            self.window.rowconfigure(row,weight=3)
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
            self.window.rowconfigure(row,weight=3)
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
                hueMax=np.percentile(hsvRoi[:,:,0],95)
                hueMin=np.percentile(hsvRoi[:,:,0],5)
                print(hueMin,hueMax)
                #caso 170-180 0-10
                if hueMin<60 and hueMax>50:
                    self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMax, np.percentile(hsvRoi[:,:,1],5), np.percentile(hsvRoi[:,:,2],5)],np.uint8)
                    self.videoObject.calibracionAuto['rojo1'][1] = np.array([180, 255, 255],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][0] = np.array([0, np.percentile(hsvRoi[:,:,1],5), np.percentile(hsvRoi[:,:,2],5)],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMin+1, 255, 255],np.uint8)
                #caso 150-179 o # 0-10
                else:
                    self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMin, np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                    self.videoObject.calibracionAuto['rojo1'][1] = np.array([hueMax, 255, 255],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][0] = np.array([hueMin, np.percentile(hsvRoi[:,:,1],15), np.percentile(hsvRoi[:,:,2],15)],np.uint8)
                    self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMax, 255, 255],np.uint8)



        btn2 = Button(self.window, text="Calibrar",font=self.font, command=calibrate, fg="black", bg="white")

        btn2.configure(bg='#6AD5D0')
        btn2.grid(column=3, row=4)

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
                        hueMax=np.percentile(rectHSV[:,:,0],97)
                        hueMin=np.percentile(rectHSV[:,:,0],3)
                        print(hueMin,hueMax)
                        #caso 170-180 0-10
                        if hueMin<60 and hueMax>50:
                            self.videoObject.calibracionAuto['rojo1'][0] = np.array([hueMax, np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                            self.videoObject.calibracionAuto['rojo1'][1] = np.array([180, 255,255],np.uint8)
                            self.videoObject.calibracionAuto['rojo2'][0] = np.array([0, np.percentile(rectHSV[:,:,1],15), np.percentile(rectHSV[:,:,2],15)],np.uint8)
                            self.videoObject.calibracionAuto['rojo2'][1] = np.array([hueMin+1, 255,255],np.uint8)
                            print(self.videoObject.calibracionAuto['rojo1'],self.videoObject.calibracionAuto['rojo2'])
                            print(self.videoObject.calibracionAuto['verde'])

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

        btn3 = Button(self.window, text="Calibrar con click",font=self.font, command=calibrateClick, fg="black", bg="white")

        btn3.configure(bg='#42D7D0')
        btn3.grid(column=4, row=4)

        def guardar():
            print('Guardando!')                
            arriba=[self.arrayElegido[0],self.arrayElegido[1],self.arrayElegido[2]]
            medio=[self.arrayElegido[3],self.arrayElegido[4],self.arrayElegido[5]]
            abajo=[self.arrayElegido[6],self.arrayElegido[7],self.arrayElegido[8]]
            self.modoNormal=[arriba,medio,abajo]
            self.guardar=True   

        
        def modoMovil():
            print('pasando a modo movil!')                
            inputValue=textBox.get("1.0","end-1c")
            print(inputValue)
            if inputValue != '':
                self.videoObject.movil['ip']=inputValue
            self.videoObject.movil['activado']=not  self.videoObject.movil['activado']
        



        btn4 = Button(self.window, text="Modo movil", font=self.font,command=modoMovil, fg="black", bg="white")
        btn4.configure(bg='#42D7D0')
        btn4.grid(column=9, row=4)

        textBox=Text(self.window,font=self.font,height=1, width=20)
        textBox.insert(INSERT ,'192.168.1.105:8080')


        textBox.configure(bg='#42D7D0')
        textBox.grid(column=5, row=4,columnspan=3)

wi= Window()
