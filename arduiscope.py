# Copyright (C) 2015 Sylvain Afchain
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import argparse
import datetime
import serial
import signal
import string
import time


class VCDFile(object):

    def __init__(self, filename):
        self._filename = filename

        self._analog_symbols = list(string.ascii_lowercase)
        self._digital_symbols = list(string.ascii_uppercase)

    def open(self):
        self._vcd = open(self._filename, "w")

    def close(self):
        self._vcd.close()

    def _write_header(self):
        self._vcd.write("$date %s $end\n" % datetime.datetime.now())
        self._vcd.write("$version arduivcd V1 $end\n")
        self._vcd.write("$timescale 1 us $end\n")
        self._vcd.write("$scope module wires $end\n")

    def _write_symbols(self):
        pin = 1
        for symbol in self._analog_symbols:
            self._vcd.write("$var wire 10 %s A_%d $end\n" % (symbol, pin))
            pin += 1

        pin = 1
        for symbol in self._digital_symbols:
            self._vcd.write("$var wire 1 %s D_%d $end\n" % (symbol, pin))
            pin += 1

    def write_value(self, pin, mode, value, time):
        self._vcd.write("#%d\n" % time)
        if mode == 'd':
            self._vcd.write(str(value) +
                            self._digital_symbols[pin - 1] + "\n")
        else:
            bin_value = str(bin(value))[1:]
            self._vcd.write(bin_value + " " +
                            self._analog_symbols[pin - 1] + "\n")

    def __enter__(self):
        self.open()
        self._write_header()
        self._write_symbols()

        return self

    def __exit__(self, type, value, traceback):
        self.close()


class ArduiScope(object):

    def __init__(self, serial_port, serial_speed, filename):
        self._filename = filename
        self._serial_port = serial_port
        self._serial_speed = serial_speed
        self._capturing = False

    def capture(self):
        self._capturing = True

        ser = serial.Serial(self._serial_port, self._serial_speed)

        last_mesure = int(time.time())

        total_duration = 0
        total_mesures = 0
        with VCDFile(self._filename) as vcd:
            while self._capturing:
                line = ser.readline()
                try:
                    pin, mode, value, duration = line.split(" ")
                    vcd.write_value(int(pin), mode, int(value), total_duration)
                    total_duration += int(duration)
                    total_mesures += 1
                except:
                    pass

                now = int(time.time())
                if now > last_mesure:
                    print "%d value(s) captured" % total_mesures
                    last_mesure = now
        print "%d value(s) captured" % total_mesures

    def stop(self):
        self._capturing = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arduino Oscilloscope')
    parser.add_argument('-d', '--device', metavar='DEVICE',
                        help='Serial device ex: /dev/xxx', required=True)
    parser.add_argument('-s', '--speed', metavar='SPEED', type=int,
                        help='Speed used for the serial device',
                        default=115200)
    parser.add_argument('-f', '--filename', metavar='FILENAME', required=True,
                        help='Ouput file path')
    args = parser.parse_args()

    arduiscope = ArduiScope(args.device, args.speed, args.filename)

    def stop_capture(signum, frame):
        arduiscope.stop()
        print "Capture stopped !"

    signal.signal(signal.SIGINT, stop_capture)

    print "Start capturing.... Ctrl-C to stop"
    arduiscope.capture()
