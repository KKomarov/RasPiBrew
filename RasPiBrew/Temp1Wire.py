import os
from subprocess import Popen, PIPE, call


class Temp1Wire:
    numSensor = 0

    def __init__(self, tempSensorId):
        self.tempSensorId = tempSensorId
        self.sensorNum = Temp1Wire.numSensor
        Temp1Wire.numSensor += 1
        # Raspbian build in January 2015 (kernel 3.18.8 and higher) has changed the device tree.
        oldOneWireDir = "/sys/bus/w1/devices/w1_bus_master1/"
        newOneWireDir = "/sys/bus/w1/devices/"
        if os.path.exists(oldOneWireDir):
            self.oneWireDir = oldOneWireDir
        else:
            self.oneWireDir = newOneWireDir
        print("Constructing 1W sensor %s" % (tempSensorId))

    def readTempC(self):
        pipe = Popen(["cat", self.oneWireDir + self.tempSensorId + "/w1_slave"], stdout=PIPE)

        result = pipe.communicate()[0].decode()
        if not result:
            return

        if result.split('\n')[0].split(' ')[11] == "YES":
            return float(result.split("=")[-1]) / 1000  # temp in Celcius
        else:
            return
