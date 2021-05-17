# Class wrapper for the ffplay read on Windows
# Windows-specific counterpart to the FIFOWriter, which was quite
# non-portable

import time
import sys
import win32pipe, win32file, pywintypes

name = "vsp-fifo"

class Win32PipeWriter:
    """Class wrapper for writing the DJI stream to a Win32 Named Pipe"""
    def __init__(self):
        self.FIFO = None
        self.LastError = None
        self.Handle = None


    def Open(self, HandleName = name):
        """Create and open a named pipe """
        # Need to get the semantics right for non-blocking with NOWAIT
        self.Handle = win32pipe.CreateNamedPipe(
            r'\\.\pipe\vsp-fifo',
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)

    def Write(self, Data):
        if self.Handle == None:
            self.LastError = "Pipe not open"
            return None
        rv = win32file.WriteFile(self.Handle, Data)
        print("WriteFile returned " + str(rv))
        return

    def Reset(self):
        return

