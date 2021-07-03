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

from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# alternative to check "from cryptography.fernet import Fernet"




class CmacAes128:
    freshness_counter = 0x00
    def __init__(self, secret_key, message, rxqueue):
        self.queue = rxqueue
        self.secret_key=secret_key
        self.message = message
        #self.freshness_value = freshness_value
        self.parseErr=0
        self.transmitted_data = []
        
    
    def start_listening(self):
        #print("Open CAN device {}".format(self.cfg['can.port']))
        print("Before initialiye bus")
        self.bus = can.interface.Bus('can1', bustype='socketcan')
        rxThread = threading.Thread(target=self.rxWorker)
        rxThread.start()
        print("thread has started")
    
    def rxWorker(self):
        
        print("Starting thread")
        while True:
            msg=self.bus.recv()
            can_data = msg.__str__()
            print(can_data)
            d = can_data[-41:-18]
            d= '0x ' + d
            d=d.replace(' ', '')
            a = int(d, 16)
            hex_a = hex(a)
            print(hex_a)
            self.transmitted_data.append(d)
            

    def calculate_complete_freshness(self, arr[]):
        for element in arr:
            # Get access to array element's 5th byte
            truncated_counter = access_nth_byte(element, 3)
            actual_pi_counter = access_nth_byte(freshness_counter, 0)
            if truncated_counter > actual_pi_counter:
            complete_counter = hex((actual_pi_counter<<8) | truncated_counter)
            print(complete_counter)
        
    def access_nth_byte(target, n):
        return hex((target&(0xFF<<(8*n)))>>(8*n))
    
    def assign_freshness(self):
        pass
        
    def generate_mac(self):
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
        print (calculated_mac)
        
        return calculated_mac
    
    def truncate_mac(self, mac):
        pass
        

        
        
    
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
