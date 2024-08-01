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

tasa_rf = 0.002  # ajustado
tasa_ab = 0.006
def calcular_tasas(listaM, listaR, listaD, listaA, listaF):
    tasa_d = GeneracionCoeficientes(listaD, 300)
    tasa_r = GeneracionCoeficientes(listaR, 300)
    tasa_m = GeneracionCoeficientes(listaM, 300)
    tasa_ap = GeneracionCoeficientes(listaA, 300)
    tasa_mf = GeneracionCoeficientes(listaF, 300)
    print(f"tasa_d {tasa_d/100}")
    print(f"tasa_r {tasa_r/100}" )
    print(f"tasa_m {tasa_m/100}" )
    print(f"tasa_ap {tasa_ap/100}" )
    print(f"tasa_mf {tasa_mf/100}" )
    return (tasa_m/1000), (tasa_r/1000), (tasa_d/1000), (tasa_ap/1000), (tasa_mf/1000)

#tasa_d = 0.23
#tasa_r = 0.1  # ajustado
#tasa_ab = 0.5  # ajustado
#tasa_rf = 0.2  # ajustado
#tasa_ap = 0.6  # ajustado
#tasa_mf = 0.15  # ajustado
#tasa_m = 0.5  # ajustado

M_max = 600
R_max = 30
D_max = 30
def funcionM(M, R, D, A, F):

    fMatriculado = tasa_m*M - tasa_d*M + tasa_mf * M
    return fMatriculado

def funcionR(M, R, D, A, F):

    fReprobados = tasa_r*M + (tasa_ab - tasa_ap) * R + tasa_rf * M
    return fReprobados

def funcionD(M, R, D, A, F):

    tasa_apd = 0.0096 #696

    fDesertores = tasa_ab*R + tasa_apd*D + tasa_mf*F - tasa_ap*A
    return fDesertores

def funcionA(M, R, D, A, F):
    tasa_apf = 0.002
    fAprobados = tasa_ap*M - tasa_r*A + tasa_apf*F#tasa_r*M - tasa_ab*M + tasa_apf*F
    return fAprobados

def funcionF(M, R, D, A, F):

    fForaneos = tasa_mf *  M - tasa_d * F
    return fForaneos



def funcionG(M, R, D, A, F, h, o):
    k11 = funcionM(M,R,D,A,F,)
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
    if (o == "M"):
        fM_1 = M + h/6 * (k11+2*k12+2*k13+k14)
        return fM_1
    if (o == "A"):
        fA_1 = A + h/6 * (k41+2*k42+2*k43+k44)
        return fA_1
    if (o == "R"):
        fR_1 = R + h/6 * (k21+2*k22+2*k23+k24)
        return fR_1
    if (o == "D"):
        fD_1 = D + h/6 * (k31+2*k32+2*k33+k34)
        return fD_1
    if (o == "F"):
        fF_1 = F + h/6 * (k51+2*k52+2*k53+k54)
        return fF_1


    #t = t+0.25  #cada 0.25 unidad representa un cuarto de año

def realizarPrediccion(listaD, listaT, listaR, listaA, listaM, listaF, anioPrediccion):
    global tasa_m, tasa_d, tasa_r, tasa_ap, tasa_ab, tasa_mf, tasa_rf
    tasa_m, tasa_r, tasa_d, tasa_ap, tasa_mf = calcular_tasas(listaM, listaR, listaD, listaA, listaF)
    anioP = panda.to_datetime(f'{2024 + anioPrediccion}-01-01')
    tPrediccion = listaT[-1]
    t = panda.to_datetime(tPrediccion)
    dias_aumentar = 15
    h = 0.1
    r = 1
    M1 = listaM[-1]
    A1 = listaA[-1]
    D1 = listaD[-1]
    R1 = listaR[-1]
    F1 = listaF[-1]
    listaTotal = []
    while t < anioP:  #t < anioP
        M1 = funcionG(M1, R1, D1, A1, F1, 0.1, "M")
        R1 = funcionG(M1, R1, D1, A1, F1, 0.1, "R")
        D1 = funcionG(M1, R1, D1, A1, F1, 0.1, "D")
        A1 = funcionG(M1, R1, D1, A1, F1, 0.1, "A")
        F1 = funcionG(M1, R1, D1, A1, F1, 0.1, "F")
        t += datetime.timedelta(days=dias_aumentar)
        h = h + 0.1
        if h >= r:
            listaD.append(round(D1))
            listaT.append(t)
            listaR.append(round(R1))
            listaA.append(round(A1))
            listaM.append(round(M1))
            listaF.append(round(F1))
            r = r + 1
    listaTotal.append(listaD)
    listaTotal.append(listaT)
    listaTotal.append(listaR)
    listaTotal.append(listaA)
    listaTotal.append(listaM)
    listaTotal.append(listaF)      
    return listaTotal

def obtener_periodos(periodos, anio):
    anioDato = 24 + anio
    ultimoPeriodo = periodos[-1]
    nuevoAnio = int(ultimoPeriodo[-2:])
    while nuevoAnio < anioDato:
        if ultimoPeriodo[:3] == 'ABR':
            nuevoPeriodo = 'OCT' + str(nuevoAnio) + '-FEB' + str(nuevoAnio+1)
            periodos.append(nuevoPeriodo)
            ultimoPeriodo = nuevoPeriodo
            nuevoAnio += 1
        else:
            nuevoPeriodo = 'ABR' + str(nuevoAnio).zfill(2) + '-AGO' + str(nuevoAnio).zfill(2)
            periodos.append(nuevoPeriodo)
            ultimoPeriodo = nuevoPeriodo
    return periodos



#Cambiar el valor de x de unidades a fecha con la funcion pandas, y como el t, no tiene demasiado impacto
#controlar su aumento para que se ejecute correctamente - luego pasar todo el codigo a una grafica dinamica
# e imlementarla como pagina web, donde pulire todos los detalles. 
    