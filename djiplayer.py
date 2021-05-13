from lib import USBDev
from lib import FIFOWriter
import time
import os
import tkinter as tk

StartPlayer = True
StatusInterval = 0.5

headset = USBDev.USBDev()
headset.StartDevCheckThread()

output = FIFOWriter.FIFOWriter()
output.Open()

# print("Writing to FIFO at " + output.FIFO)
# State globals:
BytesWritten = 0
LastStatus = 0
StatusData = dict()
StatusData['Msg'] = "Starting Up"

###############################################################################

def PrintStatus(update):
    """Update the program status"""
    global LastStatus
    now = time.time()
    if (now - LastStatus) < StatusInterval:
        return
    print(update['Msg'], end='\r')
    LastStatus = now

###############################################################################

while True:
    PrintStatus(StatusData)
    if headset.DevicePresent == False:
        # print("Waiting on headset...")
        StatusData['Msg'] = "Waiting on headset..."
        time.sleep(.5)
        continue

    packet = headset.RecvData()
    if packet == None:
        # print("RecvData() returned None: {}".format(headset.LastError.strerror))
        StatusData['Msg'] = "Device State: " + headset.DeviceStatus
        continue

    out = output.Write(packet)

    if out:
        BytesWritten += out
        StatusData['Total'] = BytesWritten
    else:
        # print("Pausing output, no readers...")
        StatusData['Msg'] = "Output buffer full, pausing output..."
        time.sleep(.5)
        continue

    # print("In write loop, error: " + str(output.LastError) + ", total bytes written: " + str(BytesWritten))
    StatusData['Msg'] = "Device State: " + headset.DeviceStatus
    # time.sleep(.5)
    # exit()