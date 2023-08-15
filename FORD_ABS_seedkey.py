

import can
import time
import os

def setup_can():
    try:
        print('Bring up CAN0....')
        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
        time.sleep(0.1)
        #bus = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=500000)
        bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=500000
        # bus = can.Bus(interface='socketcan', channel='vcan0', bitrate=250000)
        # bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        # bus = can.Bus(interface='ixxat', channel=0, bitrate=250000)
        # bus = can.Bus(interface='vector', app_name='CANalyzer', channel=0, bitrate=250000)
    except OSError:
        print('Cannot find CAN board.')
        exit()
        
    print('Ready')


def send_msg(arb_id, data, is_extended=False):
    with can.Bus() as bus:
    msg = can.Message(arb_id, data, is_extended)

    try:
        bus.send(msg)
        print(f"Message sent on {bus.channel_info}")
    except can.CanError:
        print("Message NOT sent")

def recv_msg()
    try:
        while True:
            message = bus.recv()    # Wait until a message is received.
            
            c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
            s=''
            for i in range(message.dlc ):
                s +=  '{0:x} '.format(message.data[i])
                
            print(' {}'.format(c+s))
    except KeyboardInterrupt:
        #Catch keyboard interrupt
        os.system("sudo /sbin/ip link set can0 down")
        print('\n\rKeyboard interrupt')

def key_from_seed(seed):
    
    secret = "5B 41 74 65 7D"
    s1 = int(secret[0:2],16)
    s2 = int(secret[3:5],16)
    s3 = int(secret[6:8],16)
    s4 = int(secret[9:11],16)
    s5 = int(secret[12:14],16)

    # PCM
    #s1 = 0x08
    #s2 = 0x30
    #s3 = 0x61
    #s4 = 0xa4
    #s5 = 0xc5

    seed_int = (int(seed[0:2],16)<<16) + (int(seed[3:5],16)<<8) + (int(seed[6:8],16)) 
    or_ed_seed = ((seed_int & 0xFF0000) >> 16) | (seed_int & 0xFF00) | (s1 << 24) | (seed_int & 0xff) << 16
    mucked_value = 0xc541a9

    for i in range(0,32):
        a_bit = ((or_ed_seed >> i) & 1 ^ mucked_value & 1) << 23
        v9 = v10 = v8 = a_bit | (mucked_value >> 1);
        mucked_value = v10 & 0xEF6FD7 | ((((v9 & 0x100000) >> 20) ^ ((v8 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v8 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v8 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v8 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v8 & 0x800000) >> 23));

    for j in range(0,32):
        a_bit = ((((s5 << 24) | (s4 << 16) | s2 | (s3 << 8)) >> j) & 1 ^ mucked_value & 1) << 23;
        v14 = v13 = v12 = a_bit | (mucked_value >> 1);
	mucked_value = v14 & 0xEF6FD7 | ((((v13 & 0x100000) >> 20) ^ ((v12 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v12 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v12 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v12 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v12 & 0x800000) >> 23));

    key = ((mucked_value & 0xF0000) >> 16) | 16 * (mucked_value & 0xF) | ((((mucked_value & 0xF00000) >> 20) | ((mucked_value & 0xF000) >> 8)) << 8) | ((mucked_value & 0xFF0) >> 4 << 16);

#    print "Computed key: %x" % key
#    return "%02X %02X %02X" % ( (key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff) 
    return [(key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff]

if __name__ == '__main__':
    setup_can()
    send_msg(0x760, [0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])