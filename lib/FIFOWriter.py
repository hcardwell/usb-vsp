# Class wrapper for writing the stream to a FIFO for file-like access

import os
import errno
import posix
import time
import stat

name = "/tmp/vsp-fifo"

class FIFOWriter:
    def __init__(self):
        self.FIFO = None
        self.LastError = None
        self.Handle = None

    def Open(self, HandleName = name):
        self.FIFO = HandleName
        if stat.S_ISFIFO(os.stat(self.FIFO).st_mode) == True:
            print("DEBUG: Reusing FIFO")
        else:
            os.mkfifo(self.FIFO)

        try:
            self.Handle = posix.open(self.FIFO, posix.O_RDWR | posix.O_NONBLOCK)
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
            BytesWritten = posix.write(self.Handle, Data)
        except BlockingIOError as e:
            self.LastError = "Exception in Write: {}".format(e)
            return None

        self.LastError = None
        return BytesWritten