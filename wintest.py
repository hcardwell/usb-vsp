from lib import USBDev
import time
import signal
import sys

StatusInterval = 0.5

headset = USBDev.USBDev()
headset.StartDevCheckThread()

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
    print(update['Msg'] + "               ", end='\r')
    LastStatus = now

###############################################################################

def Shutdown(sig, frame):
    global headset
    print("Caught interrupt, stopping...")
    if headset.CheckThreadRunning:
        headset.CheckThreadRunning = False
        sleep(1)
    
    exit(0)

###############################################################################

signal.signal(signal.SIGINT, Shutdown)

###############################################################################

while True:
    PrintStatus(StatusData)
    # if not PlayerProc:
    #     StartPlayer()
    
    if headset.DevicePresent == False:
        # print("Waiting on headset...")
        StatusData['Msg'] = "Waiting on headset..."
        # If we are waiting on a headset and data has been written, everything needs to be reset:
        if BytesWritten:
            BytesWritten = 0
            output.Reset()
            StartPlayer()    # Really a restart, since we're unlinking the FIFO

        # No sense being speedy on the loop when we are waiting on a human
        print(headset.LastError)
        time.sleep(.5)
        continue

    packet = headset.RecvData()
    if packet == None:
        # print("RecvData() returned None: {}".format(headset.LastError.strerror))
        StatusData['Msg'] = "Device State: " + headset.DeviceStatus
        print(headset.LastError)
        continue

    """
    out = output.Write(packet)

    if out:
        BytesWritten += out
        StatusData['Total'] = BytesWritten
    else:
        # print("Pausing output, no readers...")
        StatusData['Msg'] = "Output buffer full, pausing output..."
        time.sleep(.5)
        continue
    """

    # print("In write loop, error: " + str(output.LastError) + ", total bytes written: " + str(BytesWritten))
    StatusData['Msg'] = "Device State: " + headset.DeviceStatus
    time.sleep(.5)
    # exit()