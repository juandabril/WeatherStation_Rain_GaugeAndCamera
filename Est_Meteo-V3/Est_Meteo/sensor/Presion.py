
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import spidev

#===========================================================================
# Inicio Captura de datos Presion Barometrica SB100
#===========================================================================
def presion_Bar():
	# SPI bus
	spi = spidev.SpiDev()
	spi.open(0,0)

	# Leemos Datos SPI del MCP3008 chip

	def ReadChannel(channel):
	  adc = spi.xfer2([1,(8+channel)<<4,0])
	  data = ((adc[1]&3) << 8) + adc[2]
	  #print (" datapres: "+str(data))
	  return data

	def ConvertVolts(data,places):
		volts = (data*5)/float(1023)
		voltsmv=round(volts*1000,places)
		return voltsmv
	
	port_SB100 = 4 # Canal ADC

	adc = ReadChannel(port_SB100)
	pot_volts = ConvertVolts(adc,4)
	presion = (0.218 * pot_volts + 114)
	spi.close()
	return presion
#===========================================================================
# Fin Captura de datos Presion Barometrica SB100
#===========================================================================

