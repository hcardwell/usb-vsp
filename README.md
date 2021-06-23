# Video Socket Proxy
## What It Is:
This is a repo for Python (using pyusb) code for grabbing the live video feed from the DJI Digital FPV Goggles.  The class design is intended to facilitate a multitude of output scenarios:

- Output to a local FIFO / named pipe, suitable for piping to a local player
- A reference Python class (FIFOWriter) implemented to provide this for Linux
- A reference Python class (Win32PipeWriter) implemented to provide this for Windows

Future output scenarios:
- OBS for live streaming
- Same named pipe, but consumed as a socket and transmitted over TCP/IP using mbuffer or nc to facilitate even more remote live feeds
- Internal web server with an HLS transform, etc.

Only the first option is implemented to minimum viability in the repo at this time, with that wrapper being djiplayer.py, relying on the ffmpeg project for actual video rendering

## How it Works:
The most crucial element, which is telling the headset to start dumping video is implemented as demoed [here](https://github.com/fpv-wtf/voc-poc).  His good work is the source for that element.  I have implemented that basic capability in Python, along with a common class wrapper that handles headset detection, resets, etc. to enable a trivial wrapper script to automate the detection, initialization, and consumption of video from a headset.

The other initial class implemented in here is the FIFOWriter class, which creates a filesystem named pipe usable for transferring the raw bitstream to other sources just like a file or socket on Linux.

The video playback itself is just handled by ffplay from the FFmpeg project.  The video from the goggles appears to be a transport-stream encoded H.264 video stream.

The out-of-the-box builds of Ubuntu for the Pi 4 do not have hardware H.264 from the Pi4 (or earlier, actually) enabled and really struggle to render the video stream in pure software.  The Pi OS builds of FFmpeg do, and the units keep up fine.

## Usable Targets
Development was done on Ubuntu Linux 20.04.2 LTS, with Linux as the primary intended target. The code is testing as working on:
* Ubuntu 20.04.2 LTS x86_64
* Ubuntu 20.04.2 LTS aarch64 on Raspberry Pi 4
* Raspberry Pi OS 'Buster' 2021-03-04 armhf
* Windows 10 x86_64 works fine via winplayer.py, installation instructions pending

I have other SBCs using various RK3399 and RK3328 chipsets on which I am about to test.

## Requirements:
I am working on an installation script to handle some of the pain, but in a nutshell you just need:
* A Linux box running a GUI (Xorg / Whatever)
* FFmpeg installed and working
* Injection of the udev rules to grant user read/write access to the USB devices (see below)
* Python 3.x (tested on 3.7 and 3.9) with pyusb installed
* The sample wrapper puts ffplay in a separate lxterminal session, so lxterminal should be installed
* This code repo

## Installation:
Quick instructions that should get the code working:
```bash
mkdir -p ~/src
cd ~/src
git clone https://github.com/hcardwell/usb-vsp.git
cd usb-vsp
sudo cp install/52-dji.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo apt update
sudo apt install python3 ffmpeg lxterminal
sudo pip3 install pyusb
```
That should cover the prereqs, and you should be able to launch the existing wrapper by running:
```bash
python3 ./djiplayer.py
```

## Ugly Demo:
[Here](https://www.youtube.com/watch?v=9Zk83SX3UjU) is a very bad YouTube video showing my code in action on a Raspberry Pi 4 as well as an old Dell laptop running Ubuntu 20.04LTS.

## Other Info:
TODO