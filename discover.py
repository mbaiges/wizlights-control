import asyncio
from pywizlight import wizlight, PilotBuilder, discovery

async def main():
    bulbs = await discovery.discover_lights(broadcast_space="192.168.1.255")
    for bulb in bulbs:
        print(bulb.__dict__)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())