# Tasmota adapter
<b> Adapter to fetch data fom a sonoff device running Tasmota </b>


For bugs and ideas of improvement feel free to open an issue!

---
## Changelog:

### Version 1.1.0:

- Added automatic background value updating 

### Version 1.0.0

- Initial publish

---

## Dependant libraries:

- urllib3      ( ```pip install urllib3``` )
<br>
---
<br>

## Example of usage:
Connect to a Sonoff Pwr Device which is running Tasmota firmware

### Initialise the instance

Instanciate the class by giving it the IP adress of the device you want to connect with.

```py
tasmota = TasmotaPowerGrabber("192.168.178.104")
```

### Read the propertys of the instance

```tasmota.timestamp``` Returns the timestamp of the last update

    "2022-09-01T01:07:30"

```tasmota.online``` Returns the current connection status

    False | True

```tasmota.power``` Returns the current power consumption in [W]

    367

```tasmota.voltage``` Returns the current voltage in [V]

    235

```tasmota.current``` Returns the current current flow in [A]

    2.156

```tasmota.apparent_power``` Returns the current apparent power consumption in [VA]

    507

```tasmota.reactive_power```Returns the current reactive power consumption in [var]

    350

```tasmota.power_factor```Returns the current power factor 

    0,72

```tasmota.power_today``` Returns todays power consumption so far in [kWh]

    0.337

```tasmota.power_yesterday``` Returns yesterdays total power consumption

    0.923


---
## Example:
```py
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
```