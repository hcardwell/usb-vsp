from lib import USBDev
from lib import FIFOWriter
import time
import os
import tkinter as tk

StartPlayer = True

output = FIFOWriter.FIFOWriter()
output.Open()

headset = USBDev.USBDev()
headset.StartDevCheckThread()

print("Writing to FIFO at " + output.FIFO)
BytesWritten = 0

def PrintStatus(StatusData):
    print("Foo")

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