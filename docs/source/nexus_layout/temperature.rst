.. _data.file.temperature:

Temperature
+++++++++++

TODO: ``#X`` (example calib.dat, scan 11) - Temperature Set Point

The SPEC ``#X`` control line [#SPEC_control_lines]_ for users to describe
temperature. [#SPEC_mac]_ This control line may be used in a scan. The canonical
representation shows a setpoint in K and then C:

.. code-block::
   :linenos:

   #X 0 -273.15 (Temperature Setpoint in K and C)

But, the documentation is vague about the expected format and users may present
files where ``#X`` provides different temperatures, such as these examples:

.. code-block::
   :linenos:

   #X Control: 298.873K  Sample: 299.036K
   #X 10.00Kohm (25.0C)

Internally, the plugin will test several formats and parse (using the first
format that does not fail) for the two values shown in the next table.

============  ========================
SPEC term     canonical meaning
============  ========================
``TEMP_SP``  	The set point of the controller in ohms, volts, etc.
``DEGC_SP``  	The temperature from which the set point is derived.
============  ========================

These values will be reported in the ``NXentry`` [#NXentry]_ group
and also linked into a new ``temperature`` subgroup [#NXlog]_ of the
``sample``, as shown below:

.. code-block::
   :linenos:

   #X Control: 298.873K  Sample: 299.036K

    DEGC_SP:NX_FLOAT64 = 299.036
    TEMP_SP:NX_FLOAT64 = 298.873
    /SCAN/sample/temperature:NXlog
        value --> /SCAN/DEGC_SP
        target_value --> /SCAN/TEMP_SP

As an alternative, the *NXsensor* [#NXsensor]_ base class has additional fields
to describe temperature sensors but the additional information is not available
in a SPEC data file.

----------------

.. [#SPEC_control_lines] https://certif.com/spec_help/scans.html
.. [#SPEC_mac] https://certif.com/spec_manual/mac_3_10.html
.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NXlog] **NXlog**:   https://manual.nexusformat.org/classes/base_classes/NXlog.html
.. [#NXsensor] **NXsensor**:   https://manual.nexusformat.org/classes/base_classes/NXsensor.html
