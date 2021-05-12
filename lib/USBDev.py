import usb.core
import usb.util

# The DJI Headset should be VID 0x2ca3 and PID 0x1f
VID=0x2ca3
PID=0x1f

MagicPacket = "524d5654"

# For the bulk transfer handle, we want interface 3:
"""
    INTERFACE 3: Vendor Specific ===========================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x3
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x2
     bInterfaceClass    :   0xff Vendor Specific
     bInterfaceSubClass :   0x43
     bInterfaceProtocol :    0x1
     iInterface         :    0xb BULK Interface
      ENDPOINT 0x3: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x3 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x84: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x84 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0

"""


class USBDev:
    def __init__(self):
        self.HasStream = False
        self.DevicePresent = False       
        self.DeviceHandle = None
        self.ManuallyClaimed = False

    def PollDev(self):
        dev = usb.core.find(idVendor=VID, idProduct=PID)
        if dev is None:
            self.DevicePresent = False
            self.DeviceHandle = None
            self.DeviceCfg = None
            self.DeviceInterface = None
            self.InPoint = None
            self.OutPoint = None
        else:
            self.DevicePresent = True
            self.DeviceHandle = dev
            self.DeviceCfg = dev[0]
            self.DeviceInterface = self.DeviceCfg[(3,0)]
            # The inpoint and outpoint maybe could be enumerated via usb.util.endpoint_direction if needed:
            self.InPoint = self.DeviceInterface[1]
            self.OutPoint = self.DeviceInterface[0]

    def ClaimDev(self):
        if self.DevicePresent:
            usb.util.claim_interface(self.DeviceHandle, self.DeviceInterface)
            self.ManuallyClaimed = True

    def ReleaseDev(self):
        if self.ManuallyClaimed and self.DevicePresent:
            usb.util.release_interface(self.DeviceHandle, self.DeviceInterface)
            self.ManuallyClaimed = False

    def SendData(self, Data: bytearray):
        if not self.DeviceHandle:
            return None
        rv = self.DeviceHandle.write(self.OutPoint.bEndpointAddress, Data)
        print("DEBUG: Wrote " + str(rv) + " bytes to outpoint")
    
    def SendMagicPacket(self):
        magic = bytearray.fromhex(MagicPacket)
        self.SendData(magic)

    def RecvData(self):
        if not self.DeviceHandle:
            return None
        rv = self.DeviceHandle.read(self.InPoint.bEndpointAddress, self.InPoint.wMaxPacketSize)
        print("DEBUG: Read " + str(len(rv)) + " bytes from goggles")
        return rv