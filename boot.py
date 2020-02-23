import pycom
import os
import machine
from machine import UART
from network import WLAN, Bluetooth

pycom.wifi_on_boot(False)

wlan = WLAN()
wlan.init(mode=WLAN.STA)
wlan.deinit()
bt = Bluetooth()
bt.deinit()


machine.main('main.py')
