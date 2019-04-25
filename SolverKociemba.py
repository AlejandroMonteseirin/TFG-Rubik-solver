#Solver de Herbert Kociemba's two-phase algorithm pasado a python por tcbegley y adaptado por AlexMonteseirin

'''
             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
 ************|************|************|************
 *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
 ************|************|************|************
 *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
 ************|************|************|************
 *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
 ************|************|************|************
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|

            Blanco=F
            Rojo=U
            Azul=L
            Verde=R
            Amarillo=B
            Naranja=D
BRAVNA
'''
from Recursos.solver.solve import Solver

#Recibe los datos del virtualizador, los transforma y los envia al resolvedor
def LlamadaEntrante(datos):
    print('transformando para resolver')
    print(datos['superior']+datos['derecha']+datos['frontal']+datos['inferior']+datos['izquierda']+datos['trasera'])
    datos=datos['superior']+datos['derecha']+datos['frontal']+datos['inferior']+datos['izquierda']+datos['trasera']
    #traductor
    cuboString=''
    for casilla in datos:
        if(casilla=='blanco'):
            cuboString+='F'
            continue
        if(casilla=='rojo'):
            cuboString+='U'
            continue
        if(casilla=='azul'):
            cuboString+='L'
            continue
        if(casilla=='verde'):
            cuboString+='R'
            continue
        if(casilla=='amarillo'):
            cuboString+='B'
            continue
        if(casilla=='naranja'):
            cuboString+='D'
            continue
    print(cuboString)
    resultado=resolver(cuboString)
    return resultado

def resolver(stringCubo):
    s = Solver()
    #ejemploResuelto('UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB')         
    #s.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD') 
    try:
        s.solve(stringCubo)
        mensajeSolucionOError="La mejor solucion encontrada es"+s.solution
    except ValueError:
        mensajeSolucionOError="Cubo Erroneo, compruebelo de nuevo"
    print(mensajeSolucionOError)
    return mensajeSolucionOError