from pycoproc import Pycoproc

import machine
import pycom
import time
import utime

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from machine import RTC
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

# try:
from pymesh_config import PymeshConfig
# except:
#     from _pymesh_config import PymeshConfig

# try:
from pymesh import Pymesh
# except:
#     from _pymesh import Pymesh

def current_time():
    current_time = utime.localtime()
    return str(current_time)

def set_time(sending_mac, msg):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    print(sending_mac)
    time_from_message_string = msg[15:]
    print(time_from_message_string)
    time_from_message_tuple = tuple(map(int, time_from_message_string.split(" ")))
    print(time_from_message_tuple)
    rtc.init(time_from_message_tuple)
    msg = "Time Set"
    pymesh.send_mess(sending_mac, str(msg))
    time.sleep(2)

def send_self_info(sending_mac):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    now_time = current_time()
    node_info = str(pymesh.mesh.get_node_info())
    msg = (now_time + " self info: %s" % node_info)
    pymesh.send_mess(sending_mac, str(msg))
    time.sleep(3)

def send_battery_voltage(sending_mac):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    volts = str(py.read_battery_voltage())
    now_time = current_time()
    own_mac = str(pymesh.mesh.mesh.MAC)
    msg = (now_time + ' Mac Address %s battery level is: %s' % (own_mac, volts))
    pymesh.send_mess(sending_mac, str(msg))
    time.sleep(1.5)

def send_baro(sending_mac):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    now_time = current_time()
    mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    msg1 = (now_time + " MPL3115A2 temperature: " + str(mp.temperature())+
            " Altitude: " + str(mp.altitude()))
    pymesh.send_mess(sending_mac, str(msg1))
    time.sleep(2)
    mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    msg2 = (now_time + " Pressure: " + str(mpp.pressure()))
    pymesh.send_mess(sending_mac, str(msg2))

def send_temp(sending_mac):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    si = SI7006A20(py)
    now_time = current_time()
    msg1 = (now_time + " Temperature: " + str(si.temperature())+
            " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
    pymesh.send_mess(sending_mac, str(msg1))
    time.sleep(2)
    msg2 = (now_time + " Dew point: "+ str(si.dew_point()) + " deg C")
    pymesh.send_mess(sending_mac, str(msg2))
    time.sleep(2)
    t_ambient = 24.4
    msg3 = (now_time + " Humidity Ambient for " + str(t_ambient) + " deg C is "
            + str(si.humid_ambient(t_ambient)) + "%RH")
    pymesh.send_mess(sending_mac, str(msg3))
    time.sleep(2)

def new_message_cb(rcv_ip, rcv_port, rcv_data):
    ''' callback triggered when a new packet arrived '''
    print('Incoming %d bytes from %s (port %d):' %
            (len(rcv_data), rcv_ip, rcv_port))
    msg = rcv_data.decode("utf-8")
    if msg[:13] == "JM batt level":
        sending_mac = msg[14:]
        print(sending_mac)
        send_battery_voltage(sending_mac)
    elif msg[:12] == "JM send self":
        sending_mac = msg[13:]
        send_self_info(sending_mac)
    elif msg[:8] == "JM RESET":
        machine.reset()
    elif msg[:12] == "JM send baro":
        sending_mac = msg[13:]
        send_baro(sending_mac)
    elif msg[:12] == "JM send temp":
        sending_mac = msg[13:]
        send_temp(sending_mac)
    elif msg[:11] == "JM set time":
        sending_mac = msg[12:14]
        set_time(sending_mac, msg)
    elif msg[:10] == "JM how set":
        sending_mac = msg[11:]
        if len(sending_mac) == 0:
            print("Mac address format wrong")
        else:
            now_time = current_time()
            msg = "Current:" + now_time + " Else, year month day hours minutes seconds micros timezone"
            pymesh.send_mess(sending_mac, str(msg))
            time.sleep(2)
    else:
        print("No action required")

    for _ in range(3):
        pycom.rgbled(0x888888)
        time.sleep(.2)
        pycom.rgbled(0)
        time.sleep(.1)
    return

pycom.heartbeat(False)

# read config file, or set default values
pymesh_config = PymeshConfig.read_config()

#initialize Pymesh
pymesh = Pymesh(pymesh_config, new_message_cb)
py = Pycoproc()
rtc = RTC()
mac = pymesh.mac()
# if mac > 10:
#     pymesh.end_device(True)
if mac == 20:
     pymesh.leader_priority(255)
elif mac == 15:
     pymesh.leader_priority(250)

while not pymesh.is_connected():
    print(pymesh.status_str())
    time.sleep(3)


# def new_br_message_cb(rcv_ip, rcv_port, rcv_data, dest_ip, dest_port):
#     ''' callback triggered when a new packet arrived for the current Border Router,
#     having destination an IP which is external from Mesh '''
#     print('Incoming %d bytes from %s (port %d), to external IPv6 %s (port %d)' %
#             (len(rcv_data), rcv_ip, rcv_port, dest_ip, dest_port))
#     print(rcv_data)

#     # user code to be inserted, to send packet to the designated Mesh-external interface
#     # ...
#     return

# add current node as Border Router, with a priority and a message handler callback
# pymesh.br_set(PymeshConfig.BR_PRIORITY_NORM, new_br_message_cb)

# remove Border Router function from current node
# pymesh.br_remove()

# send data for Mesh-external, basically to the BR
# ip = "1:2:3::4"
# port = 5555
# pymesh.send_mess_external(ip, port, "Hello World")

print("done Pymesh init, forever loop, exit/stop with Ctrl+C multiple times")
# set BR with callback

while True:
    time.sleep(3)
