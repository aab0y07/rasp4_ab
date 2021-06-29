canFrames = []
canData = []
canFramesId = []
canFv = []
canMac = []
receivedData = []

with open('testLOG.log') as f:
    canFrames = f.readlines()
    count = 0

for frame in canFrames:
    count +=1
    data = frame.split()[-1]
    canData.append(data)
    print(f'{count}: {data}')
   


for data in canData:
    data = data.split('#')
    
    id = data[0]
    canFramesId.append(id)
    
    d = data[-1][0:8]
    receivedData.append(d)
    
    fv = data[-1][8:10]
    canFv.append(fv)
    
    mac = data[-1][10:16]
    canMac.append(mac)
    
    


for data in receivedData:
    print("Retreived data: " + data)

for fv in canFv:
    print("FV value: " + fv)

for mac in canMac:
    print("Mac value: " + mac)
print("Successfully done.")
f.close()
# Parse the log file




  #"ProtectLampStatus": 0,
  #"RedStopLampState": 0,
  #"AmberWarningLampStatus": 0,
  #"FlashAmberWarningLamp": 0,
  #"FlashMalfuncIndicatorLamp": 0,
  #"FlashProtectLamp": 0,
  #"FlashRedStopLamp": 0

------command to run secoc cloud ----------------------

python3 cloudFeederSecOC.py --dbc dias_simple.dbc --host  mqtt.bosch-iot-hub.com -p 8883 -u iot2@t23dc7c7e760340cdaea5f60e38af23d9 -P superkuksaiot2 -c iothub.crt -t telemetry





