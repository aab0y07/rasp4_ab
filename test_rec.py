# import cantools
# from pprint import pprint
import can





# decode message
# db = cantools.database.load_file('dias_simple.dbc') #/home/pi/kuksa-dias-ab/kuksa.val/kuksa_feeders/dbc2val/dias_simple.dbc
key = "2b7e151628aed2a6abf7158809cf4f3c"
cipher = "aabbccdd010000000000000000000000"
while True:
    file1 = open('log_dataREce.log', 'a')
    can_bus = can.interface.Bus('can1', bustype='socketcan')
    print("receive message")
    mes = can_bus.recv()
    can_data = mes.__str__()
    file1.write(can_data)
    file1.write("\n")
file1.close()

element = "0xAABBCCDD0C59A1BC"
freshness_counter = 0x010B
# Get access to array element's 5th byte
truncated_counter = element[10:12]
print(truncated_counter)
  
pi_counter_lsb = hex((freshness_counter&(0xFF<<(8*0)))>>(8*0))[2:]
print(pi_counter_lsb)
 

pi_counter_msb = hex((freshness_counter&(0xFF<<(8*1)))>>(8*1))[2:]
print(pi_counter_msb)

complete_counter = "0x" + pi_counter_msb + truncated_counter 
a = int(complete_counter,16)
res = "{0:#0{1}x}".format(a,6)
message = res.ljust(20 + len(res), '0')
print(message)


# else condition:

temp_counter_val = "0x" + pi_counter_msb
a = int(temp_counter_val,16) + 0x1
hex_n = hex(a)
complete_counter_ =  "0x" + hex_n[2:] + truncated_counter
a = int(complete_counter_,16)
h = hex(a)
print(h)



               







#for mes in can_bus:

    #print(mes.data)
    


