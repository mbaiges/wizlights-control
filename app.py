## Light

import asyncio, keyboard
from pywizlight import wizlight, PilotBuilder, discovery

# LIGHT_IP = "192.168.1.43"

# light = light = wizlight(LIGHT_IP)

BULBS = []

async def discover_bulbs():
    return await discovery.discover_lights(broadcast_space="192.168.1.255")

async def turn_on():
    for b in BULBS:
        await b.turn_on(PilotBuilder(colortemp=3500))

def turn_on_light():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(turn_on())

async def turn_off():
    for b in BULBS:
        await b.turn_off()

def turn_off_light():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(turn_off())

## App

from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Adding an icon
icon = QIcon("icon.png")

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Creating the options
menu = QMenu()
option1 = QAction("Turn On", triggered=turn_on_light)
option2 = QAction("Turn Off", triggered=turn_off_light)
menu.addAction(option1)
menu.addAction(option2)

# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)

loop = asyncio.get_event_loop()
BULBS = []
while(len(BULBS) == 0):
	print("espera")
	BULBS = loop.run_until_complete(discover_bulbs())

for b in BULBS:
    print(f"Bulb IP address: {b.ip}")

################### MUY FEO HOTKEY 
st = loop.run_until_complete(BULBS[0].updateState())
STATE = [st.pilotResult['state']]

async def hotkey(st):
    if st[0]:
        await turn_off()
        st[0] = False
    else:
        await turn_on()
        st[0] = True

keyboard.add_hotkey('F9', lambda: asyncio.run(hotkey(STATE)))

###################

app.exec_()

