from Crypto.Hash import CMAC
from Crypto.Cipher import AES

import Queue
import MACgenerator

# alternative to check "from cryptography.fernet import Fernet"

key = "2b7e151628aed2a6abf7158809cf4f3c"  
print(len(key))
cipher = "aabbccdd010000000000000000000000" 

canQueue = Queue.Queue()
    
# Create AutosarSecOC instance
secoc = MACgenerator.CmacAes128(key, cipher, canQueue)
secoc.start_listening()

calculated_mac = secoc.generate_mac()
#truncate_mac_val = secoc.truncate_mac(calculated_mac)
#print(truncate_mac_val)


#################### Initial Steps ########################

#1. Get a CAN frame
#2. Parse the CAN frame into pieces: MAC, FV, and Data

#################### MAC generation process ##################

#3. Calculate complete counter (truncated_counter, counter)
#4. Assign complete_counter to Message
#5. Calculate MAC for verification
#6. Compare the transmitted and calculated MAC
#7. Filter the CAN frames to tampered and non_tampered list

################### Verification Process ######################     

