# Class wrapper for writing the stream to a FIFO for file-like access

import os
import errno
import time
import stat

name = "/tmp/vsp-fifo"

class FIFOWriter:
    """FIFO writer class for named pipe output from the DJI headset"""
    def __init__(self):
        self.FIFO = None
        self.LastError = None
        self.Handle = None

    def Open(self, HandleName = name):
        self.FIFO = HandleName
        try:
            os.remove(self.FIFO)
        except FileNotFoundError:
            pass

        # TODO: Windows could use some love here eventually.
        os.mkfifo(self.FIFO)

        try:
            self.Handle = os.open(self.FIFO, os.O_RDWR | os.O_NONBLOCK)
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                self.LastError = "Exception in Open(): {}".format(ex)
                return
        self.LastError = None

    def Write(self, Data):
        if self.Handle == None:
            self.Open()
            if self.LastError:
                return
        
        try:
            BytesWritten = os.write(self.Handle, Data)
        except BlockingIOError as e:
            self.LastError = "Exception in Write: {}".format(e)
            return None

        self.LastError = None
        return BytesWritten

    def Reset(self):
        # Expunge / delete / recreate the FIFO for stream resets
        if self.Handle:
            os.close(self.Handle)
            self.Handle = None

        self.Open(self.FIFO)