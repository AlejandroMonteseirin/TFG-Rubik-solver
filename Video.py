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
        self.calibracion={
        "rojo": [0,125,125],
        "azul": [122,125,125],
        "blanco": [82,6,172],
        "naranja": [160,135,180],
        "verde": [55,125,151],
        "amarillo": [25,200,170],

        }
    def getFrame(self):
        contours=self.contours
        font=self.font

        ret, frame = self.cap.read()
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame = cv2.flip( frame, 1 )
        self.fijar=True

        frame2=frame
        mask = np.zeros((640, 360, 1), np.uint8)
        mask = cv2.resize(mask, (640, 360))
        frame2 = cv2.resize(frame2, (640, 360))
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_HSV2RGB)
        self.frame=frame2

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
            frame = cv2.resize(frame, (640, 360))

            cv2.drawContours(mask, contours, x, (255,255,255), -5)
            mean_val = cv2.mean(frame,mask = mask)
            #img_mask = frame[np.where(mask == 255)]
            #mean_val = np.mean(img_mask, axis=0)
            #                imagen,contorno,contorno elegido,color del contorno(media), anchura(negativo para rellenar)
            cv2.drawContours(frame, contours, x, (mean_val[0],mean_val[1],mean_val[2]), 7)
            M = cv2.moments(contours[x])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(frame,str(x), (cX , cY ), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
            if(x==4):
                self.centro=[mean_val[0],mean_val[1],mean_val[2]]

            #Sistema de puntuacion
            def ValorarColor(ColorCalibrado,ValorPantalla):
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

            PuntuacionColores={}
            colores=['blanco','rojo','verde','azul','amarillo','naranja']
            for color in colores:
                PuntuacionColores[color]=ValorarColor(self.calibracion[color],mean_val)

            self.arrayElegido[x]=min(PuntuacionColores,key = lambda x: PuntuacionColores.get(x))

            
        

            #cv2.imshow("mask", mask)
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
        #cv2.imshow("ImagenCon Contorno", frame)
        return frame,frame2
            #print(mean_val)

