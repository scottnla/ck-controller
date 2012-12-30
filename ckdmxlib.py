import socket

class PowerSupply():
    def __init__(self,host,port=6380):
        """
        host is the host ip address (10.32.0.* for PDS-60ca power supplies); port is 6380 by default.  Header is any header that is required to send
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host,self.port))
        print "Initializing host at " + str(self.host) + ":" + str(self.port)

    def write(self,data,channel=0x00):
        """
        data should be an array of up to 170 0xRRGGBB values (one for each light).
        """
        header = bytearray([0x04, 0x01, 0xdc, 0x4a, 0x01, 0x00, 0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, channel, 0x00, 0x00, 0x00, 0x96, 0x00, 0xff, 0x0f])
        rgb_data = bytearray()
        for light in data:
            rgb_data.append(light >> 16)
            rgb_data.append(light >> 8 & 0xff)
            rgb_data.append(light & 0xff)
        packetData = str(header) + str(rgb_data)
        print "Sending packet... " + str(packetData)
        self.sock.send(packetData)
