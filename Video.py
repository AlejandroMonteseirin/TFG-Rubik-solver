import numpy as np
import cv2


#La resolución nativa de mi camara es 1280x720
class Video:

    @staticmethod
    def inicializaVideo():

        return Video()

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.arrayElegido=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        font = cv2.FONT_HERSHEY_SIMPLEX
        im = cv2.imread("../Recursos/mascaraCuadradaFullHd.png")
        im = cv2.resize(im, (640, 360))

        mask = np.zeros((640, 360, 1), np.uint8)
        mask = cv2.resize(mask, (640, 360))

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        self.contours,hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(im, self.contours, -1, (0, 255, 0), 3)
        #cv2.imshow("Todos los contornos", im)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def getFrame(self):
        

        contours=self.contours
        font=self.font

        ret, frame = self.cap.read()
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.fijar=True

        frame2=frame
        mask = np.zeros((640, 360, 1), np.uint8)
        mask = cv2.resize(mask, (640, 360))
        frame2 = cv2.resize(frame2, (640, 360))
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_HSV2RGB)

        for x in range (0,len(contours)):
            mean_val = cv2.mean(frame2,mask = mask)
            if self.arrayElegido[x]=='Blanco':
                cv2.drawContours(frame2, contours, x, (255, 255, 255), -1)
            if self.arrayElegido[x]=='Azul':
                cv2.drawContours(frame2, contours, x, (40, 40, 80), -1)
            if self.arrayElegido[x]=='Verde':
                cv2.drawContours(frame2, contours, x, (100, 150, 50), -1)
            if self.arrayElegido[x]=='Rojo':
                cv2.drawContours(frame2, contours, x, (255, 0, 0), -1)
            if self.arrayElegido[x]=='Naranja':
                cv2.drawContours(frame2, contours, x, (255, 117, 20), -1)
            if self.arrayElegido[x]=='Amarillo':
                cv2.drawContours(frame2, contours, x, (255, 255, 0), -1)



        for x in range (0,len(contours)):
            mask = np.zeros((640, 360, 1), np.uint8)
            mask = cv2.resize(mask, (640, 360))
            frame = cv2.resize(frame, (640, 360))

            cnt = contours[x]
            cv2.drawContours(mask, contours, x, (255,255,255), -1)
            #print(contours)
            mean_val = cv2.mean(frame,mask = mask)
            #                imagen,contorno,contorno elegido,color del contorno(media), anchura(negativo para rellenar)
            cv2.drawContours(frame, contours, x, (mean_val[0],mean_val[1],mean_val[2]), -1)
            M = cv2.moments(contours[x])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if mean_val[1]<30:
                cv2.putText(frame,str(x)+ 'Blanco', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(self.fijar or self.arrayElegido[x]==0):
                    self.arrayElegido[x]='Blanco'
            elif mean_val[0] > 110 and mean_val[0]<130 and mean_val[2]>50 and mean_val[1]>50:
                cv2.putText(frame,str(x)+ 'Azul', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(self.fijar or self.arrayElegido[x]==0):
                    self.arrayElegido[x]='Azul'
            elif mean_val[0] > 50 and mean_val[0] < 60 and mean_val[2] > 50 and mean_val[1] > 50:
                cv2.putText(frame, str(x) + 'Verde', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(self.fijar or self.arrayElegido[x]==0):
                    self.arrayElegido[x]='Verde'
            elif mean_val[0] > 160 or mean_val[0] < 10 and mean_val[2] > 50 and mean_val[1] > 50:
                cv2.putText(frame, str(x) + 'Rojo', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(self.fijar or self.arrayElegido[x]==0):
                    self.arrayElegido[x]='Rojo'
            elif mean_val[0] > 10 and mean_val[0] < 22 and mean_val[2] > 50 and mean_val[1] > 50:
                cv2.putText(frame, str(x) + 'Naranja', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(self.fijar or self.arrayElegido[x]==0):
                    self.arrayElegido[x]='Naranja'
            elif mean_val[0] > 22 and mean_val[0] < 40 and mean_val[2] > 50 and mean_val[1] > 50:
                cv2.putText(frame, str(x) + 'Amarillo', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)
                if(self.fijar or self.arrayElegido[x]==0):
                    self.arrayElegido[x]='Amarillo'
            elif mean_val[2]<50:
                cv2.putText(frame, str(x) + 'NEGRO?', (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)

            else:
                cv2.putText(frame,str(int(round(mean_val[0])))+' '+str(int(round(mean_val[1])))+' '+str(int(round(mean_val[2]))), (cX - 20, cY - 20), font, 0.4, (255, 255, 255), 2, cv2.LINE_AA)


            #cv2.imshow("mask", mask)
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
        #cv2.imshow("ImagenCon Contorno", frame)
        return frame,frame2
            #print(mean_val)




