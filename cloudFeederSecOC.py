
"""
This script is to collect the unauthorized CAN data, 
pre-process them, and transmit the result to the DIAS-KUKSA cloud.


Prior to running this script, the following lines should be added to 
testclient.py:
# At the end of - 'def do_getValue(self, args)'
datastore = json.loads(resp)
return datastore

"""

import argparse
import json
import socket
import subprocess
import time
#import testclient
import queue
import kuksa_viss_client
import preprocessor_bosch

#my implementation
import autosar_secoc

def getConfig():
    parser = argparse.ArgumentParser()
    #parser.add_argument("-j", "--jwt", help="JWT security token file", type=str)
    parser.add_argument("--dbc", help="DBC file used to parse CAN messages", type=str)
    parser.add_argument("--host", metavar='\b', help="Host URL", type=str) # "mqtt.bosch-iot-hub.com"
    parser.add_argument("-p", "--port", metavar='\b', help="Protocol Port Number", type=str) # "8883"
    parser.add_argument("-u", "--username", metavar='\b', help="Credential Authorization Username (e.g., {username}@{tenant-id} ) / Configured in \"Bosch IoT Hub Management API\"", type=str) # "pc01@t20babfe7fb2840119f69e692f184127d"
    parser.add_argument("-P", "--password", metavar='\b', help="Credential Authorization Password / Configured in \"Bosch IoT Hub Management API\"", type=str) # "junhyungki@123"
    parser.add_argument("-c", "--cafile", metavar='\b', help="Server Certificate File (e.g., iothub.crt)", type=str) # "iothub.crt"
    parser.add_argument("-t", "--type", metavar='\b', help="Transmission Type (e.g., telemetry or event)", type=str) # "telemetry"
    #parser.add_argument("-r", "--resume", action='store_true', help="Resume the application with the accumulated data when restarting", default=False)
    # new addition
    
    #parser.add_argument("--mapping", help="VSS mapping file", type=str)
    args = parser.parse_args()
    return args



def socket_connection_on(s, host, port):
    try:
        s.connect((host, int(port))) # host and port
        print("# Socket Connected :)")
        return True
    except socket.timeout:
        print("# Socket Timeout :(")
        return False
    except socket.gaierror:
        print("# Temporary failure in name resolution :(")
        return False

def send_telemetry(host, port, comb, telemetry_queue):
    # Create a socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    if socket_connection_on(s, host, port):
        if len(telemetry_queue) != 0:
            for i in range(0, len(telemetry_queue)):
                tel = telemetry_queue.pop(0)
                p = subprocess.Popen(tel)
                print("# Popped telemetry being sent... Queue Length: " + str(len(telemetry_queue)))
                try:
                    p.wait(1)
                except subprocess.TimeoutExpired:
                    p.kill()
                    telemetry_queue.insert(0, tel)
                    print("\n# Timeout, the popped telemetry collected. Queue Length: " + str(len(telemetry_queue)))
                    telemetry_queue.append(comb)
                    print("# The current telemetry also collected. Queue Length: " + str(len(telemetry_queue)))
                    return
                except socket.gaierror:
                    s.close()
                    telemetry_queue.insert(0, tel)
                    print("\n# Temporary failure in name resolution, the popped telemetry collected. Queue Length: " + str(len(telemetry_queue)))
                    telemetry_queue.append(comb)
                    print("# The current telemetry also collected. Queue Length: " + str(len(telemetry_queue)))
                    return
                print("# Successfully done!\n")
        p = subprocess.Popen(comb)
        print("# Current telemetry being sent...")
        try:
            p.wait(1)
        except subprocess.TimeoutExpired:
            p.kill()
            telemetry_queue.append(comb)
            print("\n# Timeout, the current telemetry collected. Queue Length: " + str(len(telemetry_queue)))
            return
        except socket.gaierror:
            s.close()
            telemetry_queue.append(comb)
            print("\n# Temporary failure in name resolution, the current telemetry collected. Queue Length: " + str(len(telemetry_queue)))
            return
        print("# Successfully done!\n")
    else:
        telemetry_queue.append(comb)
        print("# The current telemetry collected, Queue Length: " + str(len(telemetry_queue)))




canQueue = queue.Queue()
# Get the pre-fix command for publishing data
args = getConfig()

# Create AutosarSecOC instance
secoc = autosar_secoc.AutosarSecOC(args.dbc, canQueue)
secoc.start_listening()

# Get a VISS-server-connected client
#client = getVISSConnectedClient(args.jwt)

# Create a BinInfoProvider instance
#binPro = preprocessor_bosch.BinInfoProvider()

# Create authentication dictionary for signals



# buffer for mqtt messages in case of connection loss or timeout
telemetry_queue = []

while True:
    # 1. Time delay
    time.sleep(0.8)
    print("\n\n\n")

    print("HELLO WORLD!")

            
    # 5. Preprocess the data set
    tel_dict = secoc.authenticated_signals()
    print("Test: " + str(tel_dict))

    # 6. Format telemetry
    tel_json = json.dumps(tel_dict)
    # Sending device data via Mosquitto_pub (MQTT - Device to Cloud)
    comb =['mosquitto_pub', '-d', '-h', args.host, '-p', args.port, '-u', args.username, '-P', args.password, '--cafile', args.cafile, '-t', args.type, '-m', tel_json]

    # 7. MQTT: Send telemetry to the cloud. (in a JSON format)
    send_telemetry(args.host, args.port, comb, telemetry_queue)


