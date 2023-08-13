# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import spidev
#===========================================================================
# Fin Captura de datos Radiacion Solar
#===========================================================================
def radiacion():
    spi = spidev.SpiDev()
    spi.open(0,0)

    def ReadChannel(channel): 
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

	
    def ConvertVolts(data,places):
	    volts = (data * 3.3) / float(1023)
	    volts = round(volts,places)
	    return volts

    portradi = 0

    adc1 = ReadChannel(portradi)    
    voltsradi = ConvertVolts(adc1,4)    
    radi = round((voltsradi / 0.00167), 4)
    spi.close()
    return radi
#===========================================================================
# Fin Captura de datos Radiacion Solar
#===========================================================================

#===========================================================================
# Inicio Captura de datos UV
#===========================================================================
def uv():
    spi = spidev.SpiDev()
    spi.open(0,0)

    def ReadChannel(channel):
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def ConvertVolts(data,places):
        volts = (data * 3.3) / float(1023)
        volts = round(volts,places)
        return volts

    portuv = 7

    adc = ReadChannel(portuv)    
    voltuv = ConvertVolts(adc,4)    
    radiuv = round((voltuv * 16 / 2.5), 4)
    spi.close()
    return radiuv
#===========================================================================
# Fin Captura de datos UV
#===========================================================================

