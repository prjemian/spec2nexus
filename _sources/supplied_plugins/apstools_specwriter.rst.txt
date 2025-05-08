
.. _apstools_specwriter_plugin:

apstools SpecWriterCallback metadata plugin
###########################################

Looks for ``#MD`` :index:`control line` control lines.
These lines contain metadata supplied to the bluesky ``RunEngine``
and recorded during the execution of a scan.  The data are stored
in a dictionary of each scan: ``scan.MD``.  If there are no
``#MD`` control lines, then ``scan.MD`` does not exist.

**see** https://prjemian.github.io/spec2nexus/source/_filewriters.html#apstools.filewriters.SpecWriterCallback

----

.. automodule:: spec2nexus.plugins.apstools_specwriter
    :members: 
    :synopsis: Bluesky metadata from apstools SpecWriterCallback.
