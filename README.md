# py9b
Ninebot/Xiaomi electric scooter communication library and tools.

## Tools
* fwupd.py - firmware flasher capable of flashing BLE/ESC/BMS 
* readregs.py - ESC/BMS register file dumper
Other tools are higly experimental.

## Requirements
* Python 2.x.x [www.python.org]
* ProgressBar [pip install progressbar]
* PySerial [pip install pyserial] - for direct serial link backend
* PyGatt [pip install pygatt] - for BLED112 dongle backend
* nRFUARTBridge [https://github.com/flowswitch/nRFUARTBridge] - for Android BLE-TCP backend
