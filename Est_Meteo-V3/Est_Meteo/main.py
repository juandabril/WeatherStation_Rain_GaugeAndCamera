# -*- coding: utf-8 -*-
# by Joel Guerrero and Milton Reyes -

import RPi.GPIO as GPIO
from datetime import datetime, date, time, timedelta
from sensor import *
from formats import *
import time
import spidev
import os
import shutil
import struct, array, io, fcntl
import ftplib
import threading
import sys
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085

StationId='_CC007'
datadir ="/home/pi/Documents/Est_Meteo/data"
dirlog="/home/pi/Documents/Est_Meteo/log"
datadir_nosend = "/home/pi/Documents/Est_Meteo/data/nosend"
logfile = time.strftime("%Y%m%d%H%M%S") +'log_CC007'+ '.txt'
formats.creartxt(logfile,dirlog)

#DEFINICION VARIABLES PARA TIEMPOS DE LECTURA Y ENVIO
intervalfile=5 # archivo cada : x minutos
intervalread=60	# lectura cada : x segundos
intervalwind=3 # Periodo de muestreo  promedio para sensor de viento: x segundos
muestras = 3
rfactor = 2.25 # factor definido por Davis
acum = [0]
dir = [0]

#DEFINICION VARIABLES PARA CONEXION FTP
ftp_servidor = 'aplicaciones.canalclima.com'
ftp_usuario = 'FtpUser'
ftp_clave = 'S3rficorp'
ftp_raiz = '/RASPBERRYCC007'

#DEFINICION DE PINES SENSORES digitales
pinws =  18 # Pin Anemometro
pinpluv = 23 #Pin Pluviometro

#DEFINICION DE ESTADO GPIO Y ASIGNACION DE ENTRADA PARA SENSORES
GPIO.setmode(GPIO.BCM) # Se establece la Board BCM
GPIO.setup(pinpluv, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Entrada Pluviometro
GPIO.setup(pinws, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Entrada Anemometro


def TempHum():
    pintemphum = 22 #Pin Sensor AM2302
    sensor = Adafruit_DHT.AM2302 #Sensor de TEMP y HUM
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pintemphum)
    if humidity is not None and temperature is not None:
        temp = '{0:0.2f}'.format(temperature)
        hum = '{0:0.1f}'.format(humidity)
        return temp, hum
    else:
        temp = "NULL"
        hum = "NULL"
        return temp, hum
		
def BMP180():
    sensor = BMP085.BMP085()
    tempIN = '{0:0.2f}'.format(sensor.read_temperature())
    presion = '{0:0.2f}'.format(sensor.read_pressure()*0.01)
    altura = '{0:0.2f}'.format(sensor.read_altitude())
    return tempIN, presion, altura

rain=0
def Pluviometro(channel):    # LECTURA INTERRUPCIONES PLUVIOMETRO
    global rain
    rain = rain+0.2
GPIO.add_event_detect(pinpluv, GPIO.FALLING, callback=Pluviometro, bouncetime=300)

def anemometro():
    global acum
    global dir
    acum = []
    dir = []
    i = 0
    periodos=int(intervalread/muestras)
    tiempofin=time.time()
    for i in range(0,periodos):
        contador = 0
        tiempoini = time.time() #Controlamos el tiempo fin del muestreo
        diferencia=0
        estado = True
        while (diferencia < muestras):
            if (GPIO.input(pinws)== 1): # Cazoletas no han abierto el Switch
                estado = False
            if (GPIO.input(pinws)== 0 and estado == False): # Cazoletas han abierto el Switch
                estado = True
                contador = contador + 1 # Cuenta la cantidad de veces que se abrio el Switch.                
            tiempofin=time.time()        
            diferencia=tiempofin-tiempoini

        velinst=((contador *(rfactor/muestras)))* 1.60934
        acum.append(velinst)  # Velocidad en Km/h
        dirinst=viento.vane()
        dir.append(dirinst)        
    return 
    
def ftpsend(filesend,datadire): # FUNCION PARA ENVIO DATOS AL FTP
    localfile= os.path.join(datadire,filesend)
    fichero_origen = localfile
    fichero_destino = filesend
    global file_local_size
    global file_remote_size
    global send
           
    try:
        f = open(fichero_origen,'rb')        
        try:
            infolocal = os.stat(fichero_origen)
            file_local_size = int(infolocal.st_size)            
            s = ftplib.FTP(ftp_servidor,ftp_usuario, ftp_clave)            
            s.cwd(ftp_raiz)
            s.storbinary('STOR '+ fichero_destino, f)
            send = True
            file_remote_size = s.size(fichero_destino)           
            f.close()
            s.quit()            
        except IOError as e:
            texterr="ERROR en conexion o envio al servidor - Archivo : "+filesend         
            shutil.move(localfile,datadir_nosend)
            send = False
            formats.grabartxt(dirlog,logfile,texterr+" "+str(e))
            f.close()
    except IOError as e:
        texterr="ERROR abriendo  el archivo local: " + filesend
        formats.grabartxt(dirlog,logfile,texterr+" "+str(e))
            
    return  

def resubmit():   
    filelist = os.listdir("/home/pi/Documents/Est_Meteo/data/nosend")
    if(filelist == 0):
        return 
    else:        
        for file in filelist:
            file_nosend= os.path.join(datadir_nosend, file) 
            ftpsend(file,datadir_nosend)
            if(send == True):                
                shutil.move(file_nosend,datadir)
        return            
              
#===========================================================================
# PROGRAMA PRINCIPAL
#===========================================================================
while True:
    k = threading.Thread(target=resubmit, args=(),name='FTPnosend')
    k.start()
    tiempoinicio = datetime.now()
    tiempofin = tiempoinicio
    archivo = time.strftime("%Y%m%d%H%M%S") +'_CC007'+ '.txt'
    formats.creartxt(archivo,datadir)
    line = 'TIEMPO,LA,T,H,VV,DV,RS,RUV,PA'
    line1 = 'TIMESTAMP,mm,C,%,Km/h,Grados,W/m2,Index,hPa'
    formats.grabartxt(datadir,archivo,line)
    formats.grabartxt(datadir,archivo,line1)
    i=0
    for i in range(0,intervalfile):
        tiempo = datetime.now()
        timeData = tiempo.strftime("%Y-%m-%d %H:%M:%S")
        try:
            temp, hum = TempHum() # Llamamos la funcion que toma los datos de la Temperatura
        except IOError as err:           
            formats.grabartxt(dirlog,logfile,"Error en funcion Temperatura y Humedad"+str(err))
        try:
            radiaci = Radiacion.radiacion() # Llamamos la funcion que toma los datos de la Radiacion Solar
        except IOError as err:
            radiaci = "NULL"
            formats.grabartxt(dirlog,logfile,"Error en funcion Radiacion"+str(err))
        try:
            uv = Radiacion.uv() # Llamamos la funcion que toma los datos de la Radiacion UV
        except IOError as err:
            uv = "NULL"
            formats.grabartxt(dirlog,logfile,"Error en funcion Radiacion UV"+str(err))
        try:
            tempinterna, bar, altura = BMP180() 
        except IOError as err:
            bar = "NULL"
            formats.grabartxt(dirlog,logfile,"Error en funcion BMP180"+str(err))
        try:         
            resultv=[]
            resultv = viento.calcviento(acum,dir)
            velprom=resultv[0]
            dirpred=resultv[1]
        except IOError as err:
            velprom = "NULL"
            dirpred = "NULL"
            formats.grabartxt(dirlog,logfile,"Error en funcion Viento"+str(err))
                
        line2 = str(timeData) +','+str(rain)+','+temp+","+hum+","+str(velprom)+","+str(dirpred)+","+str(radiaci)+","+str(uv)+","+bar+","+tempinterna+","+altura
        formats.grabartxt(datadir,archivo,line2)
        rain =0 # inicializa el valor de lluvia a cero para cada periodo 		
        contador = 0
        h = threading.Thread(target=anemometro, args=(), name='velocidad')
        h.start()
        time.sleep(intervalread)
        i=i+1        
    	    
    t = threading.Thread(target=ftpsend, args=(archivo,datadir),name='FTPProcess')
    t.start()
    
    
	