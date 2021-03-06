"""

This script is to authenticate CAN messages on the base of Autosar SecOC module

        hexSecKey = "2b7e151628aed2a6abf7158809cf4f3c"
        secret= bytearray.fromhex(hexSecKey)
        cobj = CMAC.new(secret, ciphermod=AES)
        hexMes = "aabbccdd010000000000000000000000"
        byteMes= bytearray.fromhex(hexMes)
        cobj.update(byteMes)

        print (cobj.hexdigest())


"""

# Create command to execute the script


import os
import argparse
import can
import threading
import time

import logging
import cantools
import j1939

logging.getLogger('j1939').setLevel(logging.DEBUG)
logging.getLogger('can').setLevel(logging.DEBUG)

from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# alternative to check "from cryptography.fernet import Fernet"




class CmacAes128:
    freshness_counter = 0x0000
    def __init__(self, secret_key, rxqueue):
        self.queue = rxqueue
        self.secret_key=secret_key
        self.message = ''
        
        #self.freshness_value = freshness_value
        self.parseErr=0
        self.transmitted_data = []
        self.tampered_signals = []
        self.nonTampered_signals = []
       
        
    
    def start_listening(self):
        #print("Open CAN device {}".format(self.cfg['can.port']))
        print("Before initialiye bus")
        self.bus = can.interface.Bus('can1', bustype='socketcan')
        # create the ElectronicControlUnit (one ECU can hold multiple ControllerApplications)
        ecu = j1939.ElectronicControlUnit()
        # Connect to the CAN bus
        ecu.connect(bustype='socketcan', 'can1')
        # add CA to the ECU
        ecu.add_ca(controller_application=self)
        rxThread = threading.Thread(target=self.rxWorker)
        rxThread.start()
        print("thread has started")
    
    def rxWorker(self):
        calculated_mac = ''
        print("Starting thread")
        while True:
            msg=self.bus.recv()
            can_data = msg.__str__()
            print(can_data)
            # Writing a string to file
            file1 = open('log_data.log', 'a')
            file1.write(can_data)
            file1.write("\n")
            d = can_data[-41:-18]
            print(d)
            d= '0x ' + d
            d=d.replace(' ', '')
            a = int(d, 16)
            received_frame = hex(a)[:-1]
            print('Received CAN frame: ', received_frame)
            calculated_mac = self.verify_frame(received_frame)
            transmitted_mac = received_frame[12:]
            print('Received MAC value: ',transmitted_mac)
            print('Calculated MAC value aT: ',calculated_mac)
            # Compare transmitted and calculated MAC values
            if calculated_mac == transmitted_mac:
                CmacAes128.freshness_counter += 1
                print('Incremented FV value: ' , self.freshness_counter)
                print('MAC value has been verified successfully!')
                #Assign the CAN frame to non-tampered list
                self.nonTampered_signals.append(received_frame)
                file2 = open('nonTampered_list.log', 'a') 
                file2.write(received_frame)
                file2.write("\n")
                #Opening a file
                
                
            else: 
                print('MAC value verification has failed!')
        # Retry to verify, the next attempt
                self.tampered_signals.append(received_frame)
                file3 = open('tampered_list.log', 'a') 
                file3.write(received_frame)
                file3.write("\n") 
            #self.transmitted_data.append(d)
            
     def identify_message(self, pgn):
        pgn_hex = hex(pgn)[2:] # only hex(pgn) without '0x' prefix
        for message in self.db.messages:
            message_hex = hex(message.frame_id)[-6:-2] # only hex(pgn) without '0x' prefix, priority and source address
            if pgn_hex == message_hex:
                return message
        return None
    
    
    
    def on_message(self, pgn, data):
        message = self.identify_message(pgn)
        if message != None:
            signals = message._signals
            for signal in signals:
                self.put_signal_in_status_queue(signal, data)
                print("Put in status queue {} in with value {}".format(signal, data))

   
    def put_signal_in_status_queue(self, signal, data):
        name = signal._name
        byte_order = signal._byte_order # 'little_endian' or 'big_endian'
        scale = signal._scale
        offset = signal._offset
        data_type = type(data).__name__
        val = 0
        # When data_type is "list", `decode_signal` should be used. (Byte Level)
        if data_type != "bytearray":
            start_byte = int(signal._start / 8) # start from 0
            num_of_bytes = signal._length / 8 # most likely 1 or 2
            val = self.decode_signal(start_byte, num_of_bytes, byte_order, scale, offset, data)
        # When data_type is "bytearray", `decode_byte_array` should be used. (Bit Level)
        else:
            start_bit = signal._start
            num_of_bits = signal._length
            val = self.decode_byte_array(start_bit, num_of_bits, byte_order, scale, offset, data)
        if val < signal._minimum:
            val = signal._minimum
        elif val > signal._maximum:
            val = signal._maximum
        if name in self.mapper:
            rxTime=time.time()
            if self.mapper.minUpdateTimeElapsed(name, rxTime):
                self.queue.put((name, val))
                print("Before putting to queue {} in with value {}".format(name, val))

    def calculate_complete_freshness(self, frame):
        #for element in arr:
        # Get access to array element's 5th byte
        truncated_counter = frame[10:12]
        print('Truncated counter: ', truncated_counter)
        pi_counter_lsb = hex((self.freshness_counter&(0xFF<<(8*0)))>>(8*0))[2:]
        print('Pi counter LSB: ', pi_counter_lsb)
        pi_counter_msb = hex((self.freshness_counter&(0xFF<<(8*1)))>>(8*1))[2:]
        print('Pi counter MSB:', pi_counter_msb)
        if truncated_counter > self.freshness_counter:
            # Need to be clarified, especially byte order does not work yet
            complete_counter_1 = "0x" + pi_counter_msb + truncated_counter 
            a = int(complete_counter_1,16)
            hex_n = "{0:#0{1}x}".format(a,6)
            print('Complete counter if:', hex_n)
        else:
            temp_counter_val = "0x" + pi_counter_msb
            a = int(temp_counter_val,16) + 0x1
            hex_n = hex(a)
            complete_counter_2 =  "0x" + hex_n[2:] + truncated_counter
            a = int(complete_counter_2,16)
            hex_n = "{0:#0{1}x}".format(a,6)
            print('Complete counter else:', hex_n)
        return hex_n
            


    def access_nth_byte(target, n):
        return hex((target&(0xFF<<(8*n)))>>(8*n))
    
    def assign_cipher(self, frame):
        complete_freshness_val = ''
        complete_counter_val = self.calculate_complete_freshness(frame)
        print('Received CFV: ', complete_counter_val)
        res=''
        # 1. Get complete_freshness_value
        # 2. Retrieve the message from transmitted CAN frame
        res = frame[2:10] + complete_counter_val[2:]
        self.message = res.ljust(20 + len(res), '0')
        print('Assigned message : ', self.message)
        return self.message
            
        
        
        
    def generate_mac(self, frame):
        trunc_calc_mac = ''
        self.message = self.assign_cipher(frame)
        if ''.__eq__(self.secret_key) or ''.__eq__(self.message):
            print('Key or message cannot be empty!')
            return -1
        if len(self.secret_key) < 32 or len(self.message) < 32:
            print('Key or message length is less than 16 byte')
            return -1
        secret= bytearray.fromhex(self.secret_key)
        cobj = CMAC.new(secret, ciphermod=AES)
        byteMes= bytearray.fromhex(self.message)
        cobj.update(byteMes)
        calculated_mac = cobj.hexdigest()
        print ('Calculated mac: ', calculated_mac)
        # truncate the MAC before return
        trunc_calc_mac = calculated_mac[0:6]
        print ('Truncated mac: ', trunc_calc_mac)
        return trunc_calc_mac
        
    def verify_frame(self, can_frame):
        return self.generate_mac(can_frame)
            
    
    def authenticated_signals(self):
        print("Method to return authenticated signals")
        
        auth_signals = {
          "AmbientAirTemp": 0,
          "Aftrtrtmnt1SCRCtlystIntkGasTemp": 1,
          "Aftrtratment1ExhaustGasMassFlow": 0,
          "Aftertreatment1IntakeNOx": 0,
          "Aftertreatment1OutletNOx": 0,
          "TimeSinceEngineStart": 0,
          "ActualEngPercentTorque": 0,
          "EngReferenceTorque": 0,
          "NominalFrictionPercentTorque": 0,
          "EngSpeed": 0,
          "EngSpeedAtIdlePoint1": 0,
          "EngSpeedAtPoint2": 0,
          "BarometricPress": 0,
          "EngCoolantTemp": 0,
          "EngPercentLoadAtCurrentSpeed": 0,
          "MalfunctionIndicatorLampStatus": 0 
        }
        return auth_signals
