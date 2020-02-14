import pycom
from pycoproc import Pycoproc
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

py = Pycoproc()
ANSELC_ADDR = const(0x18E)
py.poke_memory(ANSELC_ADDR, ~(1 << 7))

machine.main('main.py')
