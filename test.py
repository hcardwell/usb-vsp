from lib import USBDev
from lib import FIFOWriter
import time

"""
headset = USBDev.USBDev()
headset.StartDevCheckThread()
time.sleep(30)
headset.CheckThreadRunning = False
time.sleep(15)
"""


output = FIFOWriter.FIFOWriter()
output.Open()

headset = USBDev.USBDev()
headset.StartDevCheckThread()

print("Writing to FIFO at " + output.FIFO)
BytesWritten = 0

while True:
    if headset.DevicePresent == False:
        print("Waiting on headset...")
        time.sleep(.5)
        continue

    packet = headset.RecvData()
    if packet == None:
        print("RecvData() returned None: {}".format(headset.LastError.strerror))
        continue
    # out = output.Write(bytearray.fromhex("deadbeef00"))
    out = output.Write(packet)

    if out:
        BytesWritten += out
    else:
        print("Pausing output, no readers...")
        time.sleep(.5)
        continue


    print("In write loop, error: " + str(output.LastError) + ", total bytes written: " + str(BytesWritten))
    # time.sleep(.5)
    # exit()

# headset.PollDev()

# print(headset.DeviceHandle)
# print(headset.DeviceHandle.get_active_configuration())
# print(headset.DeviceHandle.bNumConfigurations)

"""
headset.SendMagicPacket()

with open('testout.bin', 'wb') as OutFile:
    while True:
        block = headset.RecvData()
        if block:
            OutFile.write(block)
        else:
            print("No data received")
            break
"""

