import cklib
import scipy

def testBlasts():
    #create power supply
    psu = cklib.PowerSupply("10.32.0.96")

    #attach colorblasts to the power supply
    psu.addLight(cklib.ColorBlast(psu,1))
    psu.addLight(cklib.ColorBlast(psu,4))
    psu.addLight(cklib.ColorBlast(psu,7))

    #iterate through the lights and set their state to magenta (red + cyan)
    for light in psu.lights:
        light.state = [255,0,255]

    #write to all lights connected to psu
    psu.write()

def testFlex():
    #create power supply
    psu = cklib.PowerSupply("10.32.0.96")

    #create two strings of flex lights, set their channels, and attach them to the psu
    psu.addLight(cklib.Flex(psu,0x01))
    psu.addLight(cklib.Flex(psu,0x02))

    #write data to the lights
    for light in psu.lights:
        light.state = 255*scipy.ones(light.numChannels)

    #write to all channels of the power supply (this is a bit of a hack at the moment)
    for light in psu.lights:
        psu.write(channel=light.channel)
