"""
Title: cklib
Description: Object-oriented library for controlling power supplies, lights, etc.  The basic structure is:

The Light class (and its extensions) form the primitive unit.  The light's state is manipulated directly via its state attribute.  When all lights have been manipulated, the powersupply's write method is utilized to aggregate the data into a bytestring and send it over UDP.
"""

import socket
import colorsys
import scipy

class PowerSupply():
    def __init__(self,host,port=6380):
        """
        host is the host ip address (10.32.0.* for PDS-60ca power supplies); port is 6380 by default.  Together these form a socket that is initialized.
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host,self.port))
        print "Initializing host at " + str(self.host) + ":" + str(self.port)
        self.lights = []

    def write(self,channel=0x00):
        """

        """
        #create an empty dmx universe
        rgb_data = scipy.zeros(512)
        for light in self.lights:
            currentAddress = light.startAddress
            while(currentAddress < light.startAddress + light.numChannels):
            #put the state into the array in the correct slot.
            #List index is light.startAddress - 1 to properly zero index the data
            #currentAddress - startAddress begins at one and increases to numChannel
                rgb_data[currentAddress - 1] = light.state[currentAddress - light.startAddress]
                currentAddress += 1
        #required header to send data -- don't worry about this, don't change it unless you really know what you're doing.
        header = bytearray([0x04, 0x01, 0xdc, 0x4a, 0x01, 0x00, 0x08, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, channel, 0x00, 0x00, 0x00, 0x96, 0x00, 0xff, 0x0f])
        print rgb_data
        rgb_data = bytearray(rgb_data)
        #form the packet and send it off!
        packetData = str(header) + str(rgb_data)
        #        print "Sending packet... " + str(packetData)
        self.sock.send(packetData)

    def addLight(self,light):
        self.lights.append(light)

class Light():
    """
    The light class represents one physical unit, whether it is a string of lights (like Flex) or a single wall washer (such as a ColorBlast).  Each light is associated with a power supply (psu), startAddress, and numChannels, which are all used to determine how to properly send data.  The state of the light contains its current color.
    """
    def __init__(self,psu,startAddress,numChannels,channel=0x00):
        self.psu = psu
        self.startAddress = startAddress
        self.numChannels = numChannels
        self.state = scipy.zeros(numChannels)
        self.channel = channel

    def writeRGB(self, newState):
        if len(newState) != self.numChannels:
            raise Exception
        else:
            self.state = newState

class ColorBlast(Light):
    def __init__(self,psu,startAddress):
        Light.__init__(self,psu,startAddress,numChannels=3)

class Flex(Light):
    def __init__(self,psu,channel):
        Light.__init__(self,psu,startAddress=1,numChannels=150,channel=channel)
