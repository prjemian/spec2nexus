.. _data.file.temperature:

Temperature
+++++++++++

TODO: ``#X`` (example calib.dat, scan 11) - Temperature Set Point

https://certif.com/spec_manual/mac_3_10.html

============  ========================
SPEC term     meaning
============  ========================
``TEMP_SP``  	The set point of the controller in ohms, volts, etc.
``DEGC_SP``  	The temperature from which the set point is derived.
============  ========================

https://manual.nexusformat.org/classes/base_classes/NXsensor.html#nxsensor

::

  #X Control: 298.873K  Sample: 299.036K

    DEGC_SP:NX_FLOAT64 = 299.036
    TEMP_SP:NX_FLOAT64 = 298.873
    /SCAN/sample/temperature:NXlog
        value --> /SCAN/DEGC_SP
        target_value --> /SCAN/TEMP_SP
