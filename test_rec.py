import cantools
from pprint import pprint
import can



# decode message
db = cantools.database.load_file('dias_simple.dbc') #/home/pi/kuksa-dias-ab/kuksa.val/kuksa_feeders/dbc2val/dias_simple.dbc
can_bus = can.interface.Bus('vcan0', bustype='socketcan')
print("receive message")
mes = can_bus.recv()
data = db.decode_message(mes.arbitration_id, mes.data)
pprint(data)



#sent_message = can_bus.recv()
#dbx.decode_message(sent_message.arbitration_id, sent_message.data)
#print("Decoded message" + str(decoded))
