import numpy as np
import cv2


#La resolución nativa de mi camara es 1280x720
class Video:

    @staticmethod
    def inicializaVideo():

        return Video()

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.arrayElegido=[0,0,0,0,0,0,0,0,0]
        self.modo='Normal'
        font = cv2.FONT_HERSHEY_SIMPLEX
        im = cv2.imread("./Recursos/mascaraCuadradaFullHd.png")
        im = cv2.resize(im, (640, 360))

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
                                                        #RETR_EXTERNAL  solo coje los contornos externos en vez de 2 por cada cuadrado
        self.contours,hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(im, self.contours, -1, (0, 255, 0), 3)
        #cv2.imshow("Todos los contornos", im)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.calibracionHSV={
        "rojo": [0,125,125],
        "azul": [122,125,125],
        "blanco": [82,6,172],
        "naranja": [160,135,180],
        "verde": [55,125,151],
        "amarillo": [25,200,170],
        }
        self.calibracionRGB={
        "rojo": [125,25,37],
        "azul": [15,125,190],
        "blanco": [150,150,200],
        "naranja": [200,60,80],
        "verde": [0,255,0],
        "amarillo": [180,200,120],
        }
        #valores calibracion inicial
        self.calibracionAuto={
        "naranja": [np.array([11,60,200],np.uint8),np.array([24,255,255],np.uint8)],
        "amarillo": [np.array([25,60,200],np.uint8),np.array([64,255,255],np.uint8)],
        "verde": [np.array([65,40,50],np.uint8),np.array([80,255,255],np.uint8)],
        "azul": [np.array([85,60,200],np.uint8),np.array([150,255,255],np.uint8)],
        #El rojo tiene 2 rangos 0-10 y 151-180, por como funciona el sistema HSV
        "rojo1": [np.array([151,60,200],np.uint8),np.array([180,255,255],np.uint8)],
        "rojo2": [np.array([0,60,200],np.uint8),np.array([10,255,255],np.uint8)],

        "blanco": [np.array([0,0,200],np.uint8),np.array([180,20,255],np.uint8)]
        }

        self.contador=0

    def getFrame(self):
        contours=self.contours
        font=self.font

        ret, frame = self.cap.read()
        frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameHSV=cv2.cvtColor(frameRGB, cv2.COLOR_RGB2HSV)

        self.fijar=True

        frame2=frameRGB
        mask = np.zeros((640, 360, 1), np.uint8)
        mask = cv2.resize(mask, (640, 360))
        frame2 = cv2.resize(frame2, (640, 360))
        #frame2 = cv2.cvtColor(frame2, cv2.COLOR_HSV2RGB)
        #self.frame=frame2
        if(self.modo=='Normal'):
            frameRGB = cv2.flip( frameRGB, 1 )
            for x in range (0,len(contours)):
                mean_val = cv2.mean(frame2,mask = mask)
                if self.arrayElegido[x]=='blanco':
                    cv2.drawContours(frame2, contours, x, (255, 255, 255), -1)
                if self.arrayElegido[x]=='azul':
                    cv2.drawContours(frame2, contours, x, (40, 40, 80), -1)
                if self.arrayElegido[x]=='verde':
                    cv2.drawContours(frame2, contours, x, (100, 150, 50), -1)
                if self.arrayElegido[x]=='rojo':
                    cv2.drawContours(frame2, contours, x, (255, 0, 0), -1)
                if self.arrayElegido[x]=='naranja':
                    cv2.drawContours(frame2, contours, x, (255, 117, 20), -1)
                if self.arrayElegido[x]=='amarillo':
                    cv2.drawContours(frame2, contours, x, (255, 255, 0), -1)



            for x in range (0,len(contours)):
            
                mask = np.zeros((640, 360, 1), np.uint8)
                mask = cv2.resize(mask, (640, 360))
                frameRGB = cv2.resize(frameRGB, (640, 360))
                frameHSV = cv2.resize(frameHSV, (640, 360))

                cv2.drawContours(mask, contours, x, (255,255,255), -5)
                mean_valRGB = cv2.mean(frameRGB,mask = mask)
                mean_valHSV = cv2.mean(frameHSV,mask = mask)

                #img_mask = frame[np.where(mask == 255)]
                #mean_val = np.mean(img_mask, axis=0)
                #                imagen,contorno,contorno elegido,color del contorno(media), anchura(negativo para rellenar)
                cv2.drawContours(frameRGB, contours, x, (mean_valRGB[0],mean_valRGB[1],mean_valRGB[2]), 7)
                M = cv2.moments(contours[x])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #cv2.putText(frameRGB,str(x), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(x==4):
                    self.centroRGB=[mean_valRGB[0],mean_valRGB[1],mean_valRGB[2]]
                    self.centroHSV=[mean_valHSV[0],mean_valHSV[1],mean_valHSV[2]]
                #Sistema de puntuacion
                def ValorarColorHSV(ColorCalibrado,ValorPantalla):
                    #Calculo de la similitud del Hue (H)
                    H=ColorCalibrado[0]
                    HPantalla=ValorPantalla[0]
                    res=[abs(H-HPantalla)]
                    if(H<HPantalla):
                        res.append(H+179-HPantalla) #no hace falta hacer valor absoluto siempre sera positivo
                    else:
                        res.append(abs(H-179-HPantalla)) #hace falta hacer valor absoluto por si da negativo
                    H=min(res)
                    #Calculo de la similitud de la Saturacion (S)
                    S=ColorCalibrado[1]
                    SPantalla=ValorPantalla[1]
                    S=abs(S-SPantalla)

                    #Calculo de la similitud del Value (V)
                    V=ColorCalibrado[2]
                    VPantalla=ValorPantalla[2]
                    V=abs(V-VPantalla)

                    #Pesos y resultado
                    return H*5+S*3+V

                def ValorarColorRGB(ColorCalibrado,ValorPantalla):
                    Proporcion=ColorCalibrado[0]+ColorCalibrado[1]+ColorCalibrado[2]
                    #color 0 0 0 no de division por 0
                    if(Proporcion==0):
                        Proporcion=1
                    #Calculo de la similitud del Rojo (R)
                    R=ColorCalibrado[1]/Proporcion
                    RPantalla=ValorPantalla[1]/Proporcion
                    R=abs(R-RPantalla)

                    #Calculo de la similitud de la Verde (G)
                    G=ColorCalibrado[1]/Proporcion
                    GPantalla=ValorPantalla[1]/Proporcion
                    G=abs(G-GPantalla)

                    #Calculo de la similitud del Azul (B)
                    B=ColorCalibrado[2]/Proporcion
                    BPantalla=ValorPantalla[2]/Proporcion
                    B=abs(B-BPantalla)

                    #Pesos y resultado
                    return R+G+B

                PuntuacionColoresRGB={}
                PuntuacionColoresHSV={}

                colores=['blanco','rojo','verde','azul','amarillo','naranja']
                for color in colores:
                    PuntuacionColoresRGB[color]=ValorarColorRGB(self.calibracionRGB[color],mean_valRGB)
                    PuntuacionColoresHSV[color]=ValorarColorHSV(self.calibracionHSV[color],mean_valHSV)

                elegidoRGB=min(PuntuacionColoresRGB,key = lambda x: PuntuacionColoresRGB.get(x))
                elegidoHSV=min(PuntuacionColoresHSV,key = lambda x: PuntuacionColoresHSV.get(x))

                cv2.putText(frame2,str(elegidoRGB), (cX-30 , cY-15 ), font, 0.7, (abs(mean_valRGB[0]-255), abs(mean_valRGB[1]-255), abs(mean_valRGB[2]-255)), 2, cv2.LINE_AA)
                cv2.putText(frame2,str(elegidoHSV), (cX-30 , cY+40 ), font, 0.7, (abs(mean_valRGB[0]-255), abs(mean_valRGB[1]-255), abs(mean_valRGB[2]-255)), 2, cv2.LINE_AA)
                
                if(elegidoRGB==elegidoHSV):
                    self.arrayElegido[x]=elegidoRGB
                cara=None

        if(self.modo=='Espectacular'):
            frameRGB = cv2.resize(frameRGB, (640, 360))
            frameHSV = cv2.resize(frameHSV, (640, 360))
            #Definimos el rango del color amarillo
            amarillo = cv2.inRange(frameHSV, self.calibracionAuto['amarillo'][0], self.calibracionAuto['amarillo'][1])
            #Definimos el rango del color naranja
            naranja = cv2.inRange(frameHSV, self.calibracionAuto['naranja'][0], self.calibracionAuto['naranja'][1])
            #Definimos el rango del color verde
            verde =  cv2.inRange(frameHSV, self.calibracionAuto['verde'][0], self.calibracionAuto['verde'][1])
            #Definimos el rango del color blanco
            blanco = cv2.inRange(frameHSV, self.calibracionAuto['blanco'][0], self.calibracionAuto['blanco'][1])
            #Definimos el rango del color azul
            azul = cv2.inRange(frameHSV, self.calibracionAuto['azul'][0], self.calibracionAuto['azul'][1])
            #Definimos el rango del color rojo que puede tener 2 rangos dado el Hue
            ''' Ejemplos rojo
            rojo_lower = np.array([151,150,125],np.uint8)
            rojo_upper = np.array([180,255,199],np.uint8)
            rojo2_lower = np.array([0,150,125],np.uint8)
            rojo2_upper = np.array([10,255,199],np.uint8)
            '''
            rojo1 = cv2.inRange(frameHSV, self.calibracionAuto['rojo1'][0], self.calibracionAuto['rojo1'][1])
            rojo2 = cv2.inRange(frameHSV, self.calibracionAuto['rojo2'][0], self.calibracionAuto['rojo2'][1])

            # kernal = np.ones((5 ,5), "uint8")
            #blue=cv2.dilate(yellow, kernal)
            #sumamos todas las mascaras para ver el resultado final en la pantalla de la derecha
            #res=cv2.bitwise_and(frameRGB, frameRGB, mask = amarillo+naranja+verde+blanco+azul+rojo1+rojo2)
            res=cv2.bitwise_and(frameRGB, frameRGB, mask = rojo1+rojo2)

            (contoursAmarillo,hierarchy)=cv2.findContours(amarillo,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            Cubo=[]
            for pic, contour in enumerate(contoursAmarillo):
                area = cv2.contourArea(contour)
                if(area>1000):
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #cv2.putText(frameRGB,str(Cubo), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    x,y,w,h = cv2.boundingRect(contour)     
                    frameRGB = cv2.rectangle(frameRGB,(x,y),(x+w,y+h),(255,255,0),3)
                    Cubo.append(['amarillo',cX,cY,[0,255,255]])

            (contoursNaranja,hierarchy)=cv2.findContours(naranja,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contoursNaranja):
                area = cv2.contourArea(contour)
                if(area>300):
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #cv2.putText(frameRGB,str(Cubo), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    x,y,w,h = cv2.boundingRect(contour)     
                    frameRGB = cv2.rectangle(frameRGB,(x,y),(x+w,y+h),(255,150,0),3)
                    Cubo.append(['naranja',cX,cY,[0, 128, 255] ])
            
            (contoursVerde,hierarchy)=cv2.findContours(verde,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contoursVerde):
                area = cv2.contourArea(contour)
                if(area>1000):
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #cv2.putText(frameRGB,str(Cubo), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    x,y,w,h = cv2.boundingRect(contour)     
                    frameRGB = cv2.rectangle(frameRGB,(x,y),(x+w,y+h),(0,255,0),3)
                    Cubo.append(['verde',cX,cY,[0, 255, 0] ])

            (contoursAzul,hierarchy)=cv2.findContours(azul,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contoursAzul):
                area = cv2.contourArea(contour)
                if(area>1000):
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #cv2.putText(frameRGB,str(Cubo), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    x,y,w,h = cv2.boundingRect(contour)     
                    frameRGB = cv2.rectangle(frameRGB,(x,y),(x+w,y+h),(0,0,255),3)
                    Cubo.append(['azul',cX,cY,[255, 0, 0] ])

            (contoursRojo,hierarchy)=cv2.findContours(rojo1+rojo2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contoursRojo):
                area = cv2.contourArea(contour)
                if(area>1000):
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #cv2.putText(frameRGB,str(Cubo), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    x,y,w,h = cv2.boundingRect(contour)     
                    frameRGB = cv2.rectangle(frameRGB,(x,y),(x+w,y+h),(255,0,0),3)
                    Cubo.append(['rojo',cX,cY,[0, 0, 255] ])

            (contoursBlanco,hierarchy)=cv2.findContours(blanco,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contoursBlanco):
                area = cv2.contourArea(contour)
                if(area>2000 and area <5000 and len(Cubo)<9):
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    #cv2.putText(frameRGB,str(Cubo), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                    x,y,w,h = cv2.boundingRect(contour)     
                    frameRGB = cv2.rectangle(frameRGB,(x,y),(x+w,y+h),(255,255,255),3)
                    Cubo.append(['blanco',cX,cY,[255, 255, 255] ])

            frame2=res
            frame2 = cv2.flip( frame2, 1 )
            frameRGB = cv2.flip( frameRGB, 1 )
            cv2.putText(frameRGB,str(len(Cubo))+' - '+str(self.contador), (0,50 ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)

    
            if(len(Cubo)==9):
                self.contador+=1
            elif(self.contador>0):
                self.contador+=-1
            if(self.contador>25):
                cara=Cubo
                self.contador=0
            else:
                cara=None


            cv2.rectangle(frameRGB,(260,118),(360,217),(255,255,255),3)

        return frameRGB,frame2,cara
            #print(mean_val)

