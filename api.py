from aiohttp import web
import asyncio
import os

import json
from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.controller.mixins.garage import GarageOpenerMixin
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from time import sleep

from tinydb import TinyDB, Query
from dataclasses import dataclass
from datetime import datetime

import os

EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASS')

consumption_values = []
meross = []

async def ask_meross():
    devices = []
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    await manager.async_device_discovery()
    devs = manager.find_devices(device_class=ElectricityMixin)
    

    if len(devs) < 1:
        print("No electricity-capable device found...")

    # Read the electricity power/voltage/current
    now = datetime.now()
    for dev in devs:
        for i in range(1):
            instant_consumption = await dev.async_get_instant_metrics()
            sleep(2)
            consumption_values.append(instant_consumption.power)
        
        devices.append({"type": "socket", "date": now.strftime("%d/%m/%Y, %H:%M:%S"), "name": dev.name, "consumption": instant_consumption.power})

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()
    return devices 

async def get_meross(request):
    power_data = await ask_meross()
    _ = [request.app['db'].insert(reg) for reg in power_data]
    for reg in power_data:
        if reg.get('type') == "socket":
            with open('./static/metrics', 'w') as met:
                met.write(f"{reg.get('name')} {reg.get('consumption')}\n")
                met.flush()
    return web.json_response(power_data)

app = web.Application()
os.popen('rm db.json')
app['db'] = TinyDB('./db.json')
app.add_routes([web.get('/meross', get_meross)])
web.run_app(app)
