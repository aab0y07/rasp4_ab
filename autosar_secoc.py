"""

This script is to authenticate CAN messages on the base of Autosar SecOC module


"""

# Create command to execute the script


import os
import argparse
import can, cantools
import threading
import time

class AutosarSecOC:
    
    def __init__(self, dbc, rxqueue):
        self.queue=rxqueue

        
        print("Reading dbc file")
        self.db = dbc

        #self.canidwl = self.get_whitelist()

        self.parseErr=0


    def start_listening(self):
        print("Open CAN device vcan0")
        self.bus = can.interface.Bus('vcan0', bustype='socketcan')
        rxThread = threading.Thread(target=self.rxWorker)
        rxThread.start()

    def get_whitelist(self):
        print("Collecting signals, generating CAN ID whitelist")
        wl = []
        for entry in self.mapper.map():
            #print("Passed entry: " + str(entry[0]))
            canid=self.get_canid_for_signal(entry[0])
            #print("Passed canid: " + str(canid))
            if canid != None and canid not in wl:
                wl.append(canid)
        return wl

    def get_canid_for_signal(self, sig_to_find):
        for msg in self.db.messages:
            for signal in msg.signals:
                if signal.name == sig_to_find:
                    id = msg.frame_id
                    print("Found signal {} in CAN frame id 0x{:02x}".format(signal.name, id))
                    return id
        print("Signal {} not found in DBC file".format(sig_to_find))
        return None

    def rxWorker(self):
        print("Starting thread")
        while True:
            msg=self.bus.recv()
            try:
                decode=self.db.decode_message(msg.arbitration_id, msg.data)
                #print("Decod" +str(decode))
            except Exception as e:
                self.parseErr+=1
                #print("Error Decoding: "+str(e))
                continue
            rxTime=time.time()
            for k,v in decode.items():
                if k in self.mapper:
                    if self.mapper.minUpdateTimeElapsed(k, rxTime):
                        self.queue.put((k,v))
    
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
