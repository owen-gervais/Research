import hub, import utime

uart = hub.port.B
uart.mode(hub.port.MODE_FULL_DUPLEX)
uart.baud(115200)

while(True):
    uart.write(str(hub.motion.yaw_pitch_rol()) + '\n')
    utime.sleep(0.01)
