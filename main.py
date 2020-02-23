from pycoproc import Pycoproc

import machine
import pycom
import time

# try:
from pymesh_config import PymeshConfig
# except:
#     from _pymesh_config import PymeshConfig

# try:
from pymesh import Pymesh
# except:
#     from _pymesh import Pymesh

def send_self_info(sending_mac):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    node_info = str(pymesh.mesh.get_node_info())
    msg = ("self info: %s" % node_info)
    pymesh.send_mess(sending_mac, str(msg))
    time.sleep(3)

def send_battery_voltage(sending_mac):
    if len(sending_mac) == 0:
        print("Mac address format wrong")
        return
    volts = str(py.read_battery_voltage())
    own_mac = str(pymesh.mesh.mesh.MAC)
    msg = ('Mac Address %s battery level is: %s' % (own_mac, volts))
    pymesh.send_mess(sending_mac, str(msg))
    time.sleep(1.5)

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
