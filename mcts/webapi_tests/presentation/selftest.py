# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from adb_helper import AdbHelper
from mcts_apps import MCTSApps
from mdsn import ServiceListener
from presentation_controller.controller import PresentationApiController
from zeroconf import ServiceBrowser, Zeroconf

# Get device IP for mDNS matching
device_ip = AdbHelper.adb_shell("ifconfig wlan0").split(" ")[2]

# Initial socket server for testig purpose
controller = PresentationApiController()
controller_host = controller.get_addr()
controller_port = controller.get_port()

zeroconf = Zeroconf()
flag = False
listener = ServiceListener()

# Don't need to initial marionette in real test cases
from marionette import Marionette
m = Marionette('localhost', port=2828)
m.start_session()

# Using MCTS apps for launching the app
mcts = MCTSApps(m)
mcts.launch("MCTS")

# TODO: need to find the manifest url for MCTS presentation api test app
#       should parse this information to Socket Client for json to be sent

# Start [mDNS Services Discovery]
# Listen to _mozilla_papi._tcp in local area
browser = ServiceBrowser(zeroconf, "_mozilla_papi._tcp.local.", listener)

# Keep waiting for mDNS response till device found (30 seconds)
try:
    time = 30
    while (not flag) and time >= 0:
        sleep(0.2)
        flag = listener.check_ip(device_ip)
        time = time - 0.2
finally:
    zeroconf.close()
#TODO: IP Verification Required

# Start [Client - Target Device Communication]
# Setup presentation server's host and port
controller.set_pre_action(flag[0], flag[1])

# Send message to presentation server
msg_first = '{"type":"requestSession:Init", "id":"MCTS", "url":"app://notification-receiver.gaiamobile.org/index.html", "presentationId":"presentationMCTS"}'
msg_second = '{"type":"requestSession:Offer", "offer":{"type":1, "tcpAddress":["' + controller_host + '"], "tcpPort":' + str(controller_port) + '}}'
controller.send_pre_action_message(msg_first)
controller.send_pre_action_message(msg_second)

# Receive the message from presentation sever
pre_received = controller.recv_pre_action_message()

#TODO: Verify Controller Side Data

# close socket
controller.finish_pre_action()

# Start [Client Side Server - Target Device Communication]
# Start listen
controller.start()

# Client side server sends message to target device
msg = 'This is Controller\'s first message.'
controller.sendall(msg)
print('Send: {}'.format(msg))

#TODO: App Side Verification Required

# Client side server receives data/response
controller_received = controller.recv(1024)
print('Recv: {}'.format(controller_received))

#TODO: App Side Verification Required
