.. _data.file.instrument:

Instrument
++++++++++

The ``/SCAN/instrument`` group is a NeXus **NXinstrument** [#NXinstrument]_ base
class that provides a standardized way to describe the scientific instrument. It
has provisions to describe detectors, positioners, slits, monochromators, and
many other items used.

In the sample shown here, the ``/SCAN/instrument/positioners`` group is
linked to the content in ``/SCAN/positioners``.

.. code-block::
   :linenos:

   instrument:NXinstrument
     @NX_class = "NXinstrument"
     positioners --> /S1/positioners

.. [#NXinstrument] **NXinstrument**:   https://manual.nexusformat.org/classes/base_classes/NXinstrument.html
