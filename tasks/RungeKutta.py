import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.utils import resample
import datetime
import pandas as panda


def GeneracionCoeficientes(listaY, numSimulaciones):
    listaX = np.arange(1, len(listaY) + 1).reshape(-1, 1)
    coeficientes = []
    for i in range(numSimulaciones):
        muestaX, muestraY = resample(listaX, listaY)
        modelo = LinearRegression().fit(muestaX, muestraY)
        coeficientes.append(modelo.coef_[0])
    promedioCoeficientes = np.mean(coeficientes)     
    return promedioCoeficientes
         
Di = [4, 5, 7, 8, 7, 5]   
Mi = [50, 51, 52, 52, 53, 53] #
Ri = [20, 19, 20, 19, 19, 20]
Ai = [32, 33, 34, 35, 35, 37]
Fi = [7, 8, 8, 10, 11, 9]
TAI = [12, 13, 12, 13, 12, 13]
RFI = [2, 3, 4, 3, 3, 3]
MFI = [13, 14, 15, 16, 14, 14]

tasa_d = GeneracionCoeficientes(Di, 500)   
tasa_r = GeneracionCoeficientes(Ri, 500) 
tasa_ab = GeneracionCoeficientes(TAI, 500) 
tasa_rf = GeneracionCoeficientes(RFI, 500)
tasa_ap = GeneracionCoeficientes(Ai, 500)
tasa_mf = GeneracionCoeficientes(MFI, 500)
tasa_m = GeneracionCoeficientes(Mi, 500)

#tasa_d = 0.23
#tasa_r = 0.1  # ajustado
#tasa_ab = 0.5  # ajustado
#tasa_rf = 0.2  # ajustado
#tasa_ap = 0.6  # ajustado
#tasa_mf = 0.15  # ajustado
#tasa_m = 0.5  # ajustado


def funcionM(M, R, D, A, F):
    #tasa_d = 0.23
    fMatriculado = (tasa_m - tasa_d) * M  #Hice cambio en el modelo  
    #fMatriculado = -tasa_d*M
    return fMatriculado

def funcionR(M, R, D, A, F):
    #tasa_r = 0.14 #0,14
    #tasa_ab = 1.154 #1.154
    #tasa_rf = 0.35
    fReprobados = tasa_r*M - tasa_ab*R - tasa_rf*F
    return fReprobados

def funcionD(M, R, D, A, F):
    #tasa_ap = 0.696 #696
    #tasa_ab = 0.154 #154 
    #tasa_mf = 0.25
    fDesertores = tasa_ab*R - tasa_ap*D + tasa_mf*F
    return fDesertores

def funcionA(M, R, D, A, F):
    #tasa_ap = 0.696
    fAprobados = tasa_ap*D    
    return fAprobados

def funcionF(M, R, D, A, F):
    #tasa_mf = 0.25
    #tasa_m = 0.80 
    fForaneos = tasa_mf * M - tasa_m * D - tasa_m *  F 
    return fForaneos

def funcionM_1(M, R, D, A, F, h):
    k11 = funcionM(M,R,D,A,F)
    k21 = funcionR(M,R,D,A,F)
    k31 = funcionD(M,R,D,A,F)
    k41 = funcionA(M,R,D,A,F)
    k51 = funcionF(M,R,D,A,F)
    k12 = funcionM(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2) #t+h/2
    k22 = funcionR(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k32 = funcionD(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k42 = funcionA(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k52 = funcionF(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k13 = funcionM(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k23 = funcionR(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k33 = funcionD(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k43 = funcionA(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k53 = funcionF(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k14 = funcionM(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k24 = funcionR(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k34 = funcionD(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k44 = funcionA(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k54 = funcionF(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    fM_1 = M + h/6 * (k11+2*k12+2*k13+k14)
    return fM_1

def funcionR_1(M, R, D, A, F, h):
    k11 = funcionM(M,R,D,A,F)
    k21 = funcionR(M,R,D,A,F)
    k31 = funcionD(M,R,D,A,F)
    k41 = funcionA(M,R,D,A,F)
    k51 = funcionF(M,R,D,A,F)
    k12 = funcionM(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k22 = funcionR(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k32 = funcionD(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k42 = funcionA(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k52 = funcionF(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k13 = funcionM(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k23 = funcionR(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k33 = funcionD(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k43 = funcionA(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k53 = funcionF(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k14 = funcionM(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k24 = funcionR(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k34 = funcionD(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k44 = funcionA(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k54 = funcionF(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    fR_1 = R + h/6 * (k21+2*k22+2*k23+k24)
    return fR_1

def funcionD_1(M, R, D, A, F, h):
    k11 = funcionM(M,R,D,A,F)
    k21 = funcionR(M,R,D,A,F)
    k31 = funcionD(M,R,D,A,F)
    k41 = funcionA(M,R,D,A,F)
    k51 = funcionF(M,R,D,A,F)
    k12 = funcionM(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k22 = funcionR(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k32 = funcionD(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k42 = funcionA(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k52 = funcionF(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k13 = funcionM(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k23 = funcionR(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k33 = funcionD(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k43 = funcionA(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k53 = funcionF(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k14 = funcionM(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k24 = funcionR(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k34 = funcionD(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k44 = funcionA(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k54 = funcionF(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    fD_1 = D + h/6 * (k31+2*k32+2*k33+k34)
    return fD_1

def funcionA_1(M, R, D, A, F, h):
    k11 = funcionM(M,R,D,A,F)
    k21 = funcionR(M,R,D,A,F)
    k31 = funcionD(M,R,D,A,F)
    k41 = funcionA(M,R,D,A,F)
    k51 = funcionF(M,R,D,A,F)
    k12 = funcionM(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k22 = funcionR(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k32 = funcionD(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k42 = funcionA(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k52 = funcionF(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k13 = funcionM(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k23 = funcionR(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k33 = funcionD(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k43 = funcionA(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k53 = funcionF(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k14 = funcionM(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k24 = funcionR(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k34 = funcionD(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k44 = funcionA(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k54 = funcionF(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    fA_1 = A + h/6 * (k41+2*k42+2*k43+k44)
    return fA_1

def funcionF_1(M, R, D, A, F, h):
    k11 = funcionM(M,R,D,A,F)
    k21 = funcionR(M,R,D,A,F)
    k31 = funcionD(M,R,D,A,F)
    k41 = funcionA(M,R,D,A,F)
    k51 = funcionF(M,R,D,A,F)
    k12 = funcionM(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k22 = funcionR(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k32 = funcionD(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k42 = funcionA(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k52 = funcionF(M+k11*h/2, R+k21*h/2, D+k31*h/2, A+k41*h/2, F+k51*h/2)
    k13 = funcionM(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k23 = funcionR(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k33 = funcionD(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k43 = funcionA(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k53 = funcionF(M+k12*h/2, R+k22*h/2, D+k32*h/2, A+k42*h/2, F+k52*h/2)
    k14 = funcionM(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k24 = funcionR(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k34 = funcionD(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k44 = funcionA(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    k54 = funcionF(M+k13*h, R+k23*h, D+k33*h, A+k43*h, F+k53*h)
    fF_1 = F + h/6 * (k51+2*k52+2*k53+k54)
    return fF_1


   #prueba del primer valor
DH = [4, 5, 7, 8, 7, 7]
MH = [50, 51, 52, 52, 53, 53]
RH = [20, 19, 20, 19, 19, 20]
AH = [32, 33, 34, 35, 35, 37]
FH = [7, 8, 8, 10, 11, 9]

tiempoD = ['2020-05-11', '2020-09-01', '2021-02-27', '2021-08-18', '2022-01-11', '2022-06-11'] 

M1 = 60
A1 = 45 #313
D1 = 8
R1 = 13
F1 = 7
dias_aumentar = 15
tp = '2024-02-27'
datesS = panda.to_datetime(tiempoD)
dates = datesS.to_numpy()
t = panda.to_datetime(tp)
M = [M1]
R = [R1]
A = [A1] 
F = [F1]
D = [D1]
for a in range (20):
#    tiempo.append(t)
#    tiempoD.append(t)
    M1 = funcionM_1(M1, R1, D1, A1, F1, 0.1)
    R1 = funcionR_1(M1, R1, D1, A1, F1, 0.1)
    D1 = funcionD_1(M1, R1, D1, A1, F1, 0.1)
    A1 = funcionA_1(M1, R1, D1, A1, F1, 0.1)
    F1 = funcionF_1(M1, R1, D1, A1, F1, 0.1)
    t += datetime.timedelta(days=dias_aumentar)
    M.append(M1)
    R.append(R1)
    D.append(D1)
    A.append(A1)
    F.append(F1)
    
    AH.append(A1)
    MH.append(M1)
    FH.append(F1)
    RH.append(R1)
    DH.append(D1)
    tiempoD.append(t)
    #t = t+0.25  #cada 0.25 unidad representa un cuarto de año



def lista_desertores_prediccion():
    ValoresD = [round(valor) for valor in DH]
    return ValoresD

def lista_tiempo_prediccion():
    tiempoD_format = [fecha.strftime('%Y-%m-%d') if isinstance(fecha, panda.Timestamp) else fecha for fecha in tiempoD]
    return tiempoD_format

def lista_aprobados_prediccion():
    valoresA = [round(valor) for valor in AH]
    return valoresA

def lista_matriculados_prediccion():
    valoresM = [round(valor) for valor in MH]
    return valoresM    


def lista_reprobados_prediccion():
    valoresR = [round(valor) for valor in RH]
    return valoresR


def lista_foraneos_prediccion():
    valoresF = [round(valor) for valor in FH]
    return valoresF


def tiempo_final_historico():
    return '2024-02-27'

#Cambiar el valor de x de unidades a fecha con la funcion pandas, y como el t, no tiene demasiado impacto
#controlar su aumento para que se ejecute correctamente - luego pasar todo el codigo a una grafica dinamica
# e imlementarla como pagina web, donde pulire todos los detalles. 
    