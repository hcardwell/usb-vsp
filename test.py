from lib import USBDev

headset = USBDev.USBDev()


headset.PollDev()

# print(headset.DeviceHandle)
# print(headset.DeviceHandle.get_active_configuration())
# print(headset.DeviceHandle.bNumConfigurations)

for cfg in headset.DeviceHandle:
    print(str(cfg.bConfigurationValue))
    for intf in cfg:
        print('\t' + \
                         str(intf.bInterfaceNumber) + \
                         ',' + \
                         str(intf.bAlternateSetting) + \
                         '\n')

        for ep in intf:
            print('\t\t' + \
                             str(ep.bEndpointAddress) + \
                             '\n')


print("Direct Access:")
for ep in headset.DeviceInterface:
    print('\t\t' + \
        str(ep.bEndpointAddress) + \
        '\n')

print("Inpoint is " + str(headset.InPoint))
print("Outpoint is " + str(headset.OutPoint))

headset.SendMagicPacket()

with open('testout.bin', 'wb') as OutFile:
    while True:
        block = headset.RecvData()
        if block:
            OutFile.write(block)
        else:
            print("No data received")
            break
