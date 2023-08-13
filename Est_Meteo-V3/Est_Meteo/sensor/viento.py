# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from datetime import datetime, date, time, timedelta
from math import *
import time
import spidev


#===========================================================================
# Captura de datos de la Direccion del Viento
#===========================================================================
def vane():
    # Declaracion SPI
    spi = spidev.SpiDev()
    spi.open(0,0) # Abrimos la interfaz SPI, Los canales de MCP3008 son del 0 al 7

    # Funcion de Lectura de Datos

    def ReadChannel(channel):
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    PortDir= 2 # Canal Direccion Viento
	
    adc = ReadChannel(PortDir)

    def map_1(x, fromLow, fromHigh, toLow, toHigh): # Funcion Map que Asigna un valor de un rango a Otro
	    return int((x - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow)

    direccion = map_1(adc, 0, 1023, 0, 360) # Aplicamos Mapeo al valor del adc para llevarlo a valores 0 - 360
    if (direccion > 360): # Nos aseguramos que el valor se encuentre en el rango correcto
	    direccion = direccion - 360
    if (direccion < 0):
	    direccion = direccion + 360
    spi.close()
    return direccion

#===========================================================================
# Fin Captura de datos de la Direccion del Viento
#===========================================================================
#===========================================================================
# Verificacion de ajustes de Angulo de acuerdo al cuadrante
#===========================================================================
def cuadrante(X,Y,Angulo): # Calculo Coordenadas Sexagesimales
    if (X > 0 and Y>0):
        return abs(Angulo)
    elif (X > 0 and Y<0):
        return 180-abs(Angulo)
    elif (X < 0 and Y>0):
        return 360-abs(Angulo)
    elif (X < 0 and Y<0):
        return 180+abs(Angulo)
#===========================================================================
# Calculo Velocidad Promedio y Direccion Predominante
#===========================================================================
#===========================================================================
# Calculo Velocidad Promedio y Direccion Predominante
#===========================================================================
def calcviento(VelData,DirData):
    salida=[]
    if len(VelData)==len(DirData):
        XData=[]
        YData=[]
        x=0
        for x in range(0,len(VelData)):
            Vel=VelData[x]
            Dir=DirData[x]
            Dirrad=radians(Dir)
            XComp=Vel*sin(Dirrad)
            YComp=Vel*cos(Dirrad)
            XData.append(XComp)
            YData.append(YComp)
            x=x+1
        SumX=sum(XData)
        SumY=sum(YData)
        if(SumX == 0):
            salida=[0,Dir]
        else:
            PartX=pow(SumX,2)
            PartY=pow(SumY,2)
            PartXY=PartX+PartY
            N2=pow(len(XData),2)
            Vr=sqrt((PartXY/N2))
            Angulo=round(degrees(atan((SumX/SumY))),0)
            DirPred= cuadrante(SumX,SumY,Angulo)
            salida.append(round(Vr,2))
            salida.append(DirPred)
    else:
        print("LOS DOS VECTORES NO TIENE EL MISMO TAMAÑO")
    return salida
#===========================================================================
# Fin Calculo Velocidad Promedio y Direccion Predominante
#===========================================================================




