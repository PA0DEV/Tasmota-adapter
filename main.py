import tasmota_adapter
from time import sleep

tasmota = tasmota_adapter.TasmotaPowerGrabber("192.168.178.104")
while True:
    print(tasmota.timestamp)
    print(tasmota.online)
    print(tasmota.power)
    print(tasmota.voltage)
    print(tasmota.current)
    print(tasmota.power_factor)
    print(tasmota.power_today)
    print(tasmota.power_yesterday)
    print()
    sleep(1)