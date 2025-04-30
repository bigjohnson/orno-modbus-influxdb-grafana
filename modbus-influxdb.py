#!/usr/bin/env python3
import io
import minimalmodbus
import struct
import serial
import time
import os
from influxdb import InfluxDBClient
from timeloop import Timeloop
from datetime import timedelta
from datetime import datetime
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

MAXERRORS = 5

METERID = 1

SMARTMETER_COMPORT = '/dev/ttyS1'
SMARTMETER_ADDRESS = 1

INFLUX_HOST = 'INSERTYOURDATA'
INFLUX_PORT = 8086
INFLUX_USER = 'INSERTYOURDATA'
INFLUX_PASSWORD = 'INSERTYOURDATA'
INFLUX_DBNAME = 'INSERTYOURDATA'
INFLUX_MEASUREMENT = 'INSERTYOURDATA'

READ_INTERVAL = 10
#LOOPRUN = True
INFLUX_CLIENT = InfluxDBClient(INFLUX_HOST,
                            INFLUX_PORT,
                            INFLUX_USER,
                            INFLUX_PASSWORD,
                            INFLUX_DBNAME)
try:
    SMARTMETER = minimalmodbus.Instrument(SMARTMETER_COMPORT, SMARTMETER_ADDRESS) # port name, slave address (in decimal)
except:
    print('non posso aprire la porta', SMARTMETER_COMPORT)
    os._exit(1)

SMARTMETER.serial.baudrate = 9600         # Baud
SMARTMETER.serial.bytesize = 8
SMARTMETER.serial.parity   = serial.PARITY_EVEN # vendor default is EVEN
SMARTMETER.serial.stopbits = 1
SMARTMETER.serial.timeout  = 1          # seconds
SMARTMETER.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
SMARTMETER.clear_buffers_before_each_transaction = True
SMARTMETER.debug = False # set to "True" for debug mode

tl = Timeloop()
@tl.job(interval=timedelta(seconds=READ_INTERVAL))
def sample_job_every_10s():
    #print ('-------------------*********************-------------------')
    #global LOOPRUN
    #if LOOPRUN == True:
    #    LOOPRUN = False
        now = datetime.now()
        error = 0
        Frequency = 'no'
        while Frequency == 'no' and error <= MAXERRORS:
            try:
                Frequency = SMARTMETER.read_register(304, 2, 3, True)
                print (now, ',', Frequency, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading Frequency from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        Voltage = 'no'
        while Voltage == 'no' and error <= MAXERRORS:
            try:
                Voltage = SMARTMETER.read_register(305, 2, 3, True)
                print (Voltage, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading Voltage from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        Current = 'no'
        while Current == 'no' and error <= MAXERRORS:
            try:
                Current = SMARTMETER.read_long(313, 3, False, 0)
                print (Current / 1000, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading Current from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        ActivePower = 'no'
        while ActivePower == 'no' and error <= MAXERRORS:
            try:
                ActivePower = SMARTMETER.read_long(320, 3, False, 0)
                print (ActivePower, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading ActivePower from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        ReactivePower = 'no'
        while ReactivePower == 'no' and error <= MAXERRORS:
            try:
                ReactivePower = SMARTMETER.read_long(328, 3, False, 0)
                print (ReactivePower, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading ReactivePower from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        ApparentPower = 'no'
        while ApparentPower == 'no' and error <= MAXERRORS:
            try:
                ApparentPower = SMARTMETER.read_long(336, 3, False, 0)
                print (ApparentPower, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading ApparentPower from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        PowerFactor = 'no'
        while PowerFactor == 'no' and error <= MAXERRORS:
            try:
                PowerFactor = SMARTMETER.read_register(344, 3, 3, True)
                print (PowerFactor, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading PowerFactor from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        ActiveEnergy = 'no'
        while ActiveEnergy == 'no' and error <= MAXERRORS:
            try:
                ActiveEnergys = SMARTMETER.read_registers(40960, 10, 3)  # registeraddress, number_of_decimals=0, functioncode=3, signed=False
                bits = (ActiveEnergys[0] << 16) + ActiveEnergys[1] # combining Total Energy valuepair
                s = struct.pack('>i', bits) # write to string an interpret as int
                tmp = struct.unpack('>L', s)[0] # extract from string and interpret as unsigned long
                ActiveEnergy = tmp/100 # needs to be converted
                print (ActiveEnergy, ',', end='', sep="")
            except:
                error += 1
                eprint ("Error reading ActiveEnergy from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        error = 0
        ReactiveEnergy = 'no'
        while ReactiveEnergy == 'no' and error <= MAXERRORS:
            try:
                ReactiveEnergys = SMARTMETER.read_registers(40990, 10, 3)  # registeraddress, number_of_decimals=0, functioncode=3, signed=False
                bits = (ReactiveEnergys[0] << 16) + ReactiveEnergys[1] # combining Total Energy valuepair
                s = struct.pack('>i', bits) # write to string an interpret as int
                tmp = struct.unpack('>L', s)[0] # extract from string and interpret as unsigned long
                ReactiveEnergy = tmp/100 # needs to be converted
                print (ReactiveEnergy)
            except:
                error += 1
                eprint ("Error reading ReactiveEnergy from meter at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
        if Frequency != 'no' and \
         Voltage != 'no' and \
         Current != 'no' and \
         ActivePower != 'no' and \
         ReactivePower != 'no' and \
         ApparentPower != 'no' and \
         PowerFactor != 'no' and \
         ActiveEnergy != 'no' and \
         ReactiveEnergy != 'no':
            json_body = [
                {
                    'measurement': INFLUX_MEASUREMENT,
                    'tags': {
                        'meter': METERID,
                    },
                    'fields': {
                        "Frequency" : float(Frequency),
                        "Voltage" : float(Voltage),
                        "Current" : float(Current),
                        "ActivePower" : ActivePower,
                        "ReactivePower" : ReactivePower,
                        "ApparentPower" : ApparentPower,
                        "PowerFactor" : float(PowerFactor),
                        "ActiveEnergy" : float(ActiveEnergy),
                        "ReactiveEnergy" : float(ReactiveEnergy)
                    }
                }
            ]
            try:
                INFLUX_CLIENT.write_points(json_body)
                #print("writing")
            except:
                eprint('Influx write error!')
        else:
            eprint("Error reading instrument at address", SMARTMETER_ADDRESS, "on", SMARTMETER_COMPORT)
    #    LOOPRUN = True
    #else:
    #    eprint("Skipped loop run!")

if __name__ == "__main__":  #main loop
    tl.start(block=True)

