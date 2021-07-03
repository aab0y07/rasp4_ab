# import cantools
# from pprint import pprint
import can





# decode message
# db = cantools.database.load_file('dias_simple.dbc') #/home/pi/kuksa-dias-ab/kuksa.val/kuksa_feeders/dbc2val/dias_simple.dbc
key = "2b7e151628aed2a6abf7158809cf4f3c"
cipher = "aabbccdd010000000000000000000000"
#can_bus = can.interface.Bus('can1', bustype='socketcan')
print("receive message")
#mes = can_bus.recv()



a = 0xff
b = 0x11

print hex((a<<8) | b)






#for mes in can_bus:

    #print(mes.data)
    


