#import RPi.GPIO as GPIO
from datetime import datetime, date, time, timedelta
#from sensor import *
from formats import *  # install everytime # no va## import formats
import time
#import spidev  # install everytime  #pending for compatibility
import os
import shutil
import struct, array, io#, fcntl
import ftplib
import threading
import sys
#import Adafruit_DHT 
#import Adafruit_BMP.BMP085 as BMP085

StationId='_CC007'
datadir ="/home/admin/Est001/data"
dirlog="/home/admin/Est001/log"
datadir_nosend ="/home/admin/Est001/data/no_send"
logfile = time.strftime("%Y%m%d%H%M%S") +'log_CC007'+ '.txt'
##formats.creartxt(logfile,dirlog)

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
ftp_raiz = 'testraspberry'#'/RASPBERRYCC007'  ### Configure 

pinpluv = 23 #Pin Pluviometro
##GPIO.setup(pinpluv, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Entrada Pluviometro

def Pluviometro(channel):    # LECTURA INTERRUPCIONES PLUVIOMETRO
    global rain
    rain = rain+0.2
##GPIO.add_event_detect(pinpluv, GPIO.FALLING, callback=Pluviometro, bouncetime=300)

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
    filelist = os.listdir("/home/admin/Est001/data/no_send")
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
    ## Network configuration
    # Connect to WLAN

    ##  FTP 
    k = threading.Thread(target=resubmit, args=(),name='FTPnosend')
    k.start()
    tiempoinicio = datetime.now()
    tiempofin = tiempoinicio
    archivo = time.strftime("%Y%m%d%H%M%S") +'_CC007'+ '.txt'
    formats.creartxt(archivo,datadir)
    line = 'TIEMPO,RainFalling'#,T,H,VV,DV,RS,RUV,PA'
    line1 = 'TIMESTAMP,mm'#,C,%,Km/h,Grados,W/m2,Index,hPa'
    formats.grabartxt(datadir,archivo,line)
    formats.grabartxt(datadir,archivo,line1)
    i=0
    for i in range(0,intervalfile):
        tiempo = datetime.now()
        timeData = tiempo.strftime("%Y-%m-%d %H:%M:%S")

        line2 = str(timeData) +','+' prueba'#str(rain)#+','+temp+","+hum+","+str(velprom)+","+str(dirpred)+","+str(radiaci)+","+str(uv)+","+bar+","+tempinterna+","+altura
        formats.grabartxt(datadir,archivo,line2)
        rain =0 # inicializa el valor de lluvia a cero para cada periodo 		
        contador = 0
        #h = threading.Thread(target=anemometro, args=(), name='velocidad')
        #h.start()
        time.sleep(intervalread)
        i=i+1        
    	    
    t = threading.Thread(target=ftpsend, args=(archivo,datadir),name='FTPProcess')
    t.start()
    
    
	