# Class wrapper for the ffplay read on Windows
# Windows-specific counterpart to the FIFOWriter, which was quite
# non-portable

import time
import sys
import win32pipe, win32file, pywintypes

name = r'\\.\pipe\vsp-fifo'

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
            HandleName,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)
        self.FIFO = HandleName

    def Write(self, Data):
        if self.Handle == None:
            self.LastError = "Pipe not open"
            return None

        try:
            # WriteFile() returns (ErrCode, BytesWritten)
            rv = win32file.WriteFile(self.Handle, Data)
        # TODO get the WriteFile() exception types?
        except BlockingIOError as e:
            self.LastError = "Exception in Write: {}".format(e)
            return None

        self.LastError = None

        # print("WriteFile returned " + str(rv))
        return rv[1]

    def Reset(self):
        if self.Handle:
            self.Handle.Close()

        self.Open(self.FIFO)
        return

    def Close(self):
        if self.Handle:
            self.Handle.Close()
            self.Handle = None