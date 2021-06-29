import cantools
from pprint import pprint
import can


# decode message
dbx = cantools.database.load_file('dias_simple.dbc') #/home/pi/kuksa-dias-ab/kuksa.val/kuksa_feeders/dbc2val/dias_simple.dbc
print(dbx.messages)

message = dbx.get_message_by_name('EC1')

pprint(message.signals)
pprint(message.frame_id)




print("send message")

can_bus = can.interface.Bus('vcan0', bustype='socketcan')
data = message.encode({'Aftrtrtmnt1SCRCtlystIntkGasTemp': 250.1})
mess = can.Message(arbitration_id=message.frame_id, data=data)
can_bus.send(mess)

#print("receive message")
#mes = can_bus.recv()
#db.decode_message(mes.arbitration_id, mes.data)

#can_bus = can.interface.Bus('vcan0', bustype='socketcan')

#sent_message = can_bus.recv()
#dbx.decode_message(sent_message.arbitration_id, sent_message.data)
#print("Decoded message" + str(decoded))
