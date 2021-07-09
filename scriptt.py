f = open("candump_Org.log", "r+")
text = f.read().replace('can1', 'vcan0')
f.write(text)
f.close()

