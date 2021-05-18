@echo off

python -m venv vsp-venv

call vsp-venv\Scripts\activate.bat

pip install pyusb pywin32