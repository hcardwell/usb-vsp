from lib import USBDev
from lib import Win32PipeWriter
import time
import signal
import sys
import subprocess

StatusInterval = 0.5
FFplayBin = r'c:\ffmpeg\current\bin\ffplay.exe'

# Set up the input:
headset = USBDev.USBDev()
headset.StartDevCheckThread()

# And the output:
output = Win32PipeWriter.Win32PipeWriter()
output.Open()

# And the player instance, tied to the FIFO handle
PlayCmd = (FFplayBin,
    "-fs",
    "-i", output.FIFO,
    "-analyzeduration", "1",
    "-probesize", "32",
    "-sync", "ext"
)
PlayerProc = None

# State globals:
BytesWritten = 0
LastStatus = 0
StatusData = dict()
StatusData['Msg'] = "Starting Up"

###############################################################################

def StartPlayer():
    """Launch an ffplay instance to play the stream"""
    global PlayCmd, PlayerProc

    if PlayerProc:
        PlayerProc.terminate()
        PlayerProc.kill()
        PlayerProc = None

    # PlayerProc = subprocess.Popen(WrapPlayCmd)
    PlayerProc = subprocess.Popen(PlayCmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
        )


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

    if PlayerProc:
        PlayerProc.terminate()
        PlayerProc.kill()
        PlayerProc = None

    output.Close()

    # Pause for thread collection:
    time.sleep(1)
    
    exit(0)

###############################################################################

signal.signal(signal.SIGINT, Shutdown)
StartPlayer()

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
            time.sleep(1)
            StartPlayer()    # Really a restart, since we're unlinking the FIFO

        # No sense being speedy on the loop when we are waiting on a human
        time.sleep(.5)
        """
        if headset.LastError:
            print("DEBUG: " + str(headset.LastError))
        """
        continue

    packet = headset.RecvData()
    if packet == None:
        # print("RecvData() returned None: {}".format(headset.LastError.strerror))
        StatusData['Msg'] = "Device State: " + headset.DeviceStatus
        print(headset.LastError)
        continue

    out = output.Write(packet)

    if out:
        BytesWritten += out
        StatusData['Total'] = BytesWritten
    """
    else:
        # print("Pausing output, no readers...")
        StatusData['Msg'] = "Output buffer full, pausing output..."
        time.sleep(.5)
        continue
    """

    # print("In write loop, error: " + str(output.LastError) + ", total bytes written: " + str(BytesWritten))
    StatusData['Msg'] = "Device State: " + headset.DeviceStatus
    # exit()