#! /usr/bin/env python
"""
Provides a class to fetch data from a Sonoff PowR1 module running Tasmota firmware.
Link to the Tasmota firmware: https://tasmota.github.io/install/

"""

__author__ = "PA0DEV"
__copyright__ = "Copyright 2022, PA0DEV"

__licence__ = "MIT"
__version__ = "1.1.0"
__maintainer__ = "PA0DEV"
__status__ = "Development"

import json
from time import sleep
import requests
import threading
import urllib3


class TasmotaPowerGrabber():
    """
    Class to connect to a Sonoff PowR1 device running Tasmota
    """
    __online = False
    __timestamp = ""
    __voltage = 0
    __current = 0.0
    __power = 0
    __apparent_power = 0
    __reactive_power = 0
    __power_factor = 0.0
    __power_today = 0
    __power_yesterday = 0


    def __init__(self, station_ip: str) -> None:
        """
        Initiate the devicce:

        Params:
            station_ip: IP adress of the station
        """
        self.__ip = station_ip
        self.start()
        

    def start(self) -> None:
        """
        Start the connection and update the attributes automatticly
        """
        self.__thread = threading.Thread(target=self.__run)
        self.__thread.daemon = True
        self.__thread.start()


    def stop(self) -> None:
        """
        Stop the connection to the Tasmota device
        """
    
    def __run(self) -> None:
        """
        The daemon to run the automatic connection and 
        update the values
        """
        while True:
            try:
                r = requests.get(f"http://{self.__ip}/cm?cmnd=Status 8", timeout=10)

                if r.status_code != 200:
                    # request was not successfull
                    self.__online = False
                else:
                    """
                    Returns following JSON object:
                    {
                        "StatusSNS": {
                            "Time": "2022-09-01T01:07:30",
                            "ENERGY": {
                                "TotalStartTime": "2020-12-11T16:15:26",
                                "Total": 1048.895,
                                "Yesterday": 0.923,
                                "Today": 0.337,
                                "Power": 367,
                                "ApparentPower": 507,
                                "ReactivePower": 350,
                                "Factor": 0.72,
                                "Voltage": 235,
                                "Current": 2.156
                            }
                        }
                    }
                    """
                    data = json.loads(r.content)

                    self.__timestamp = data["StatusSNS"]["Time"]
                    self.__power_yesterday = data["StatusSNS"]["ENERGY"]["Yesterday"]
                    self.__power_today = data["StatusSNS"]["ENERGY"]["Today"]
                    self.__power = data["StatusSNS"]["ENERGY"]["Power"]
                    self.__apparent_power = data["StatusSNS"]["ENERGY"]["ApparentPower"]
                    self.__reactive_power = data["StatusSNS"]["ENERGY"]["ReactivePower"]
                    self.__power_factor = data["StatusSNS"]["ENERGY"]["Factor"]
                    self.__voltage = data["StatusSNS"]["ENERGY"]["Voltage"]
                    self.__current = data["StatusSNS"]["ENERGY"]["Current"]
                                           
                    self.__online = True
            except requests.exceptions.ConnectTimeout as e:
                # GET request timed out
                self.__online = False
            
            sleep(1)

    def update_values(self) -> bool:
        """
        Update station data
            
        Returns:
            True if the update was sucessfull | False if there was an error
        """
        r = requests.get(f"http://{self.__ip}/cm?cmnd=Status 8", timeout=5)

        # print(f"Status code: {r.status_code}")


        if r.status_code != 200:
            # request was not successfull
            return False
        else:
            """
            Returns following JSON object:
            {
                "StatusSNS": {
                    "Time": "2022-09-01T01:07:30",
                    "ENERGY": {
                        "TotalStartTime": "2020-12-11T16:15:26",
                        "Total": 1048.895,
                        "Yesterday": 0.923,
                        "Today": 0.337,
                        "Power": 367,
                        "ApparentPower": 507,
                        "ReactivePower": 350,
                        "Factor": 0.72,
                        "Voltage": 235,
                        "Current": 2.156
                    }
                }
            }
            """
            data = json.loads(r.content)

            self.__timestamp = data["StatusSNS"]["Time"]
            self.__power_yesterday = data["StatusSNS"]["ENERGY"]["Yesterday"]
            self.__power_today = data["StatusSNS"]["ENERGY"]["Today"]
            self.__power = data["StatusSNS"]["ENERGY"]["Power"]
            self.__apparent_power = data["StatusSNS"]["ENERGY"]["ApparentPower"]
            self.__reactive_power = data["StatusSNS"]["ENERGY"]["ReactivePower"]
            self.__power_factor = data["StatusSNS"]["ENERGY"]["Factor"]
            self.__voltage = data["StatusSNS"]["ENERGY"]["Voltage"]
            self.__current = data["StatusSNS"]["ENERGY"]["Current"]
            return True
 
    @property
    def voltage(self) -> int:
        """
        Voltage at the station
        """
        return self.__voltage
    
    @property
    def current(self) -> int:
        """
        Current at the Station
        """
        return self.__current
    
    @property
    def power(self) -> int:
        """
        Power at the station
        """
        return self.__power
    
    @property
    def apparent_power(self) -> int:
        """
        Apparent power at the Station
        """
        return self.__apparent_power
    
    @property
    def reactive_power(self) -> int:
        """
        Reactive power at the station
        """
        return self.__reactive_power
    
    @property
    def power_factor(self) -> int:
        """
        Power factor at the station
        """
        return self.__power_factor
    
    @property
    def power_today(self) -> int:
        """
        Used power since 00:00 today
        """
        return self.__power_today
    
    @property
    def power_yesterday(self) -> int:
        """
        Total power used yesterday
        """
        return self.__power_yesterday
    
    @property
    def timestamp(self) -> str:
        """
        Timestamp of the last update
        """
        return self.__timestamp

    @property
    def online(self) -> bool:
        """
        Connection status
        """
        return self.__online


if __name__ == "__main__":
    tasmota = TasmotaPowerGrabber("192.168.178.104")
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