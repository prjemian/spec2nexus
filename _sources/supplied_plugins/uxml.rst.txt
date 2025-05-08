
.. _uxml_plugin:

#UXML: UXML metadata plugin
#############################

Looks for ``#UXML`` :index:`control line` control lines.
These lines contain metadata written as XML structures
and formatted according to the supplied XML Schema ``uxml.xsd`` 
in the same directory as the ``uxml.py`` plugin.
The lines which comprise the XML are written as a list in 
each scan: ``scan.UXML``.  If there are no
``#UXML`` control lines, then ``scan.UXML`` does not exist.

Once the scan has been fully read ``scan.UXML`` is converted
into an XML document structure (using the *lxml.etree* package) 
which is stored in ``scan.UXML_root``.  The structure is validated
against the XML Schema ``uxml.xsd``.  If invalid, the error message 
is reported by raising a ``UXML_Error`` python exception.

A fully-validated structure can be written using the 
:class:`~spec2nexus.writer.Writer` class.  The UXML metadata is
written to the scan's ``NXentry`` group as subgroup named ``UXML``
with NeXus base class ``NXnote``.  The hierarchy within this ``UXML``
is defined from the content provided in the SPEC scan.

Please consult the XML Schema file for the rules governing the
use of ``#UXML`` in a SPEC data file: 
* :download:`uxml.xsd <../../../spec2nexus/plugins/uxml.xsd>`
 

----

.. automodule:: spec2nexus.plugins.uxml
    :members: 
    :synopsis: #UXML: UXML structured metadata.
