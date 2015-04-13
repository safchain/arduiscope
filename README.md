ArduiScope
==========

Very simple oscilloscope arduino library which export values in VCD format.

This library captures value from an aduino pin and sends values to the serial
where a python listens in order to write a VCD file.
The VCD file produced can be read with a VCD Viewer like GtkWave.

Installation
------------

Just copy the ArduiScope folder from the arduino folder to the libraries folder
of the Arduino IDE. An example will appear in the File menu.

Arduino part
------------

    #include "ArduiScope.h"

    ArduiScope *arduiscope;

    void setup() {
      int i;

      pinMode(2, INPUT);
      Serial.begin(115200);

      /* capture digital value of the pin 2. Mode can be DIGITAL or ANALOG */
      arduiscope = new ArduiScope(2, DIGITAL);
    }

    void loop() {
      arduiscope->capture();
    }

Computer part
-------------

In order to get the captured values from the serial device a python script has
to be used as following:

    sudo python arduiscope.py -d /dev/ttyUSB0  -f /tmp/test.vcd

The result
----------

The file produced can be read a VCD file viewer like GtkWave.

The analog pins a prefixed by A and the digital pins by D.

[![GtkWave Snapshot](https://github.com/safchain/arduiscope/doc/gtkwave.png)](https://github.com/safchain/arduiscope/doc/gtkwave.png)

LICENSE
-------

Copyright 2015, Sylvain Afchain <safchain@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

