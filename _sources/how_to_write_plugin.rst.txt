
.. _how_to_write_plugin:

How to write a custom control line handling plugin module for *spec*
######################################################################

.. sidebar:: The code to write plugins has changed with release 2021.0.0.

   The changes are summarized in the :ref:`howto_changes_plugin_2022_release`
   and :ref:`howto_changes_plugin_2021_release` sections below.

**Sections**

* :ref:`howto_load_plugin`
* :ref:`howto_write_plugin`
* :ref:`howto_example_PV_control_line`
* :ref:`howto_example_Y_control_line`
* :ref:`howto_postprocessing`
* :ref:`howto_example_postprocessing`
* :ref:`howto_summary_example`
* :ref:`howto_writer`
* :ref:`custom_key_match_function`
* :ref:`howto_summary_requirements`
* :ref:`howto_changes_plugin_2021_release`
* :ref:`howto_footnotes`

A custom plugin module for :mod:`spec2nexus.spec` is provided in 
a python module (Python source code file).
In this custom plugin module are subclasses for each *new* 
:ref:`control line <control_line_table>` 
to be supported.  An exception will 
be raised if a custom plugin module tries to provide support 
for an existing control line.  


.. _howto_load_plugin:

Load a plugin module
******************** 

Control line handling plugins for *spec2nexus* will automatically
register themselves when their module is imported.

.. code-block:: python
   :linenos:

   import pathlib
   import spec2nexus.plugin_core
   import spec2nexus.spec
   
   # load each custom plugin file:
   path = pathlib.Path("my_plugin_file.py").absolute()
   spec2nexus.plugin_core.install_user_plugin(path)
   
   # read a SPEC data file, scan 5
   spec_data_file = spec2nexus.spec.SpecDataFile("path/to/spec/datafile")
   scan5 = spec_data_file.getScan(5)

.. _howto_write_plugin:

Write a plugin module
*********************

Give the custom plugin module a name ending with ``.py``. As with any Python
module, the name must be unique within a directory. If the plugin is not in your
working directory, there must be a ``__init__.py`` file in the same directory
(even if that file is empty) so that your plugin module can be loaded with
``import <MODULE>``.

Please view the existing plugins in :mod:`~spec2nexus.plugins.spec_common` for
examples.  The custom plugin module should contain, at minimum one subclass of
:class:`~spec2nexus.plugin_core.ControlLineBase` which allows them to register
themselves when their module is imported. A custom plugin module can contain
many such handlers, as needs dictate.

.. sidebar:: *tip* : import ``strip_first_word()``

   It is also to import the :meth:`~spec2nexus.utils.strip_first_word` 
   utility method.

These imports are necessary to to write plugins for *spec2nexus*:

.. code-block:: python
   :linenos:

   from spec2nexus.plugin_core import ControlLineBase
   from spec2nexus.utils import strip_first_word

.. sidebar:: regular expressions

   There are several regular expression testers available on the web.
   Try this one, for example: https://regexpal.com/

**Attribute: ``key`` (required)**

Each subclass must define :index:`!key` ``key`` as a regular expression match for the 
control line key.  
It is possible to override any of the supplied plugins for scan :index:`control line`
control lines.
Caution is advised to avoid introducing instability.

**Attribute: ``scan_attributes_defined`` (optional)**

If your plugin creates any attributes to the
:class:`~spec2nexus.spec.SpecDataScan()` object (such as the hypothetical
``scan.hdf5_path`` and ``scan.hdf5_file``), you declare the new attributes in
the ``scan_attributes_defined`` list.  Such as this:

.. code-block:: python
   :linenos:

   scan_attributes_defined = ['hdf5_path', 'hdf5_file']

**Method: ``process()`` (required)**

Each subclass must also define a :meth:`process` method to process the control line.
A :class:`NotImplementedError` exception is raised if ``key`` is not defined.

**Method: ``match_key()`` (optional)**

For difficult regular expressions (or other situations), it is possible to replace
the function that matches for a particular control line key.  Override the
handler's :meth:`match_key` method.
For more details, see the section :ref:`custom_key_match_function`.

**Method: ``postprocess()`` (optional)**

For some types of control lines, processing can only be completed
*after* all lines of the scan have been read.  In such cases, add
a line such as this to the ``process()`` method::

    scan.addPostProcessor(self.key, self.postprocess)

(You *could* replace ``self.key`` here with some other text.  
If you do, make sure that text will be unique as it is used 
internally as a python dictionary key.)
Then, define a ``postprocess()`` method in your handler::

    def postprocess(self, scan, *args, **kws):
    	# handle your custom info here

See section :ref:`howto_postprocessing` below for more details.
See :mod:`~spec2nexus.plugins.spec_common` for many examples.

**Method: ``writer()`` (optional)**

Writing a NeXus HDF5 data file is one of the main goals of the *spec2nexus*
package.  If you intend data from your custom control line handler to
end up in the HDF5 data file, add a line such as this to either the ``process()``
or ``postprocess()`` method::

	scan.addH5writer(self.key, self.writer)

Then, define a ``writer()`` method in your handler.  Here's an example::

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """Describe how to store this data in an HDF5 NeXus file"""
        desc='SPEC positioners (#P & #O lines)'
        group = makeGroup(h5parent, 'positioners', nxclass, description=desc)
        writer.save_dict(group, scan.positioner)

See section :ref:`howto_writer` below for more details.

.. _howto_example_PV_control_line:

Full Example: **#PV** control line
**********************************

Consider a SPEC data file (named ``pv_data.txt``) with the contrived 
example of a **#PV** control 
line that associates a mnemonic with an EPICS process variable (PV).
Suppose we take this control line content to be two words (text 
with no whitespace):

.. literalinclude:: _static/pv_data.txt
    :tab-width: 4
    :linenos:
    :emphasize-lines: 14-16
    :language: text

A plugin (named ``pv_plugin.py``) to handle the ``#PV`` control lines could be written as:

.. literalinclude:: _static/pv_plugin.py
    :tab-width: 4
    :linenos:
    :language: python

When the scan parser encounters the **#PV** lines in our SPEC data file, 
it will call this
:meth:`process()` code with the full text of the line and the 
spec scan object where 
this data should be stored.  
We will choose to store this (following the pattern of other data 
names in :class:`~spec2nexus.spec.SpecDataFileScan`) as 
``scan_obj.EPICS_PV`` using a dictionary.

It is up to the user what to do with the ``scan_obj.EPICS_PV`` data.
We will not consider the ``write()`` method in this example.
(We will not write this infromation to a NeXus HDF5 file.)

We can then write a python program (named ``pv_example.py``) that will 
load the data file and interpret it using our custom plugin:

.. literalinclude:: _static/pv_example.py
    :tab-width: 4
    :linenos:
    :language: python


The output of our program:

.. code-block:: text
	:linenos:

	known:  False
	known:  True
	False
	True
	OrderedDict([('mr', 'ioc:m1'), ('ay', 'ioc:m2'), ('dy', 'ioc:m3')])


.. _howto_example_Y_control_line:

Example to ignore a **#Y** control line
***************************************

Suppose a control line in a SPEC data file must be ignored.
For example, suppose a SPEC file contains this control line: ``#Y 1 2 3 4 5``.
Since there is no standard handler for this control line, 
we create one that ignores processing by doing nothing:

.. code-block:: python
   :linenos:

   from spec2nexus.plugin_core import ControlLineBase
   
   class Ignore_Y_ControlLine(ControlLineBase):
       '''
       **#Y** -- as in ``#Y 1 2 3 4 5``
       
       example: ignore any and all #Y control lines
       '''
   
       key = '#Y'
       
       def process(self, text, spec_obj, *args, **kws):
           pass	# do nothing

.. _howto_postprocessing:

Postprocessing
**************

Sometimes, it is necessary to defer a step of processing until after the complete
scan data has been read.  One example is for 2-D or 3-D data that has been acquired
as a vector rather than matrix.  The matrix must be constructed only after all the 
scan data has been read.  Such postprocessing is handled in a method in a plugin file.
The postprocessing method is registered from the control line handler by calling the
:meth:`addPostProcessor` method of the ``spec_obj`` argument received by the 
handler's :meth:`process` method.  A key name [#]_ is supplied when registering to avoid 
registering this same code more than once.  The postprocessing function will be called 
with the instance of :class:`~spec2nexus.spec.SpecDataFileScan` as its only argument.

An important role of the postprocessing is to store the result in the scan object.
It is important not to modify other data in the scan object.  Pick an attribute
named similarly to the plugin (e.g., MCA configuration uses the **MCA** attribute, 
UNICAT metadata uses the **metadata** attribute, ...)  This attribute will define
where and how the data from the plugin is available.  The :meth:`writer` method
(see :ref:`below <howto_writer>`) is one example of a user of this attribute.


.. _howto_example_postprocessing:

Example postprocessing
======================

Consider the **#U** control line example above.  For some contrived reason,
we wish to store the sum of the numbers as a separate number, but only after 
all the scan data has been read.  This can be done with the simple expression:

.. code-block:: python
   :linenos:

   spec_obj.U_sum = sum(spec_obj.U)

To build a postprocessing method, we write:

.. code-block:: python
   :linenos:

   def contrived_summation(scan):
       '''
       add up all the numbers in the #U line
       
       :param SpecDataFileScan scan: data from a single SPEC scan
       '''
       scan.U_sum = sum(scan.U)

To register this postprocessing method, place this line in the :meth:`process`
of the handler:

.. code-block:: python
   :linenos:

   spec_obj.addPostProcessor('contrived_summation', contrived_summation)

.. _howto_summary_example:

Summary Example Custom Plugin with postprocessing
=================================================

Gathering all parts of the examples above, the custom plugin module is:

.. code-block:: python
   :linenos:

   from spec2nexus.plugin_core import ControlLineBase
   from spec2nexus.utils import strip_first_word
   
   class User_ControlLine(ControlLineBase):
       '''**#U** -- User data (#U user1 user2 user3)'''
   
       key = '#U'
       
       def process(self, text, spec_obj, *args, **kws):
           args = strip_first_word(text).split()
           user1 = float(args[0])
           user2 = float(args[1])
           user3 = float(args[2])
           spec_obj.U = [user1, user2, user3]
           spec_obj.addPostProcessor('contrived_summation', contrived_summation)


   def contrived_summation(scan):
       '''
       add up all the numbers in the #U line
       
       :param SpecDataFileScan scan: data from a single SPEC scan
       '''
       scan.U_sum = sum(scan.U)
   
   
   class Ignore_Y_ControlLine(ControlLineBase):
       '''**#Y** -- as in ``#Y 1 2 3 4 5``'''
   
       key = '#Y'
       
       def process(self, text, spec_obj, *args, **kws):
           pass

.. _howto_writer:

Custom HDF5 writer
******************

A custom HDF5 writer method defines how the data from the 
:ref:`plugin <howto_postprocessing>`
will be written to the HDF5+NeXus data file.  The writer will
be called with several arguments:

**h5parent**: *obj* : the HDF5 group that will hold this plugin's data 

**writer**:   *obj* : instance of :class:`~spec2nexus.writer.Writer()` that manages the content of the HDF5 file

**scan**:     *obj* : instance of :class:`~spec2nexus.spec.SpecDataFileScan()` containing this scan's data

**nxclass**:  *str* : (optional) name of NeXus base class to be created

Since the file is being written according to the NeXus data standard [#]_,
use the NeXus base classes [#]_ as references for how to structure the data
written by the custom HDF5 writer.  

One responsibility of a custom HDF5 writer method is to create
*unique* names for every object written in the *h5parent* group.
Usually, this will be a *NXentry* [#]_ group.  You can determine the
NeXus base class of this group using code such as this:

.. code-block:: python
   :linenos:

   >>> print h5parent.attrs['NX_class']
   <<< NXentry

Choice of NeXus base class
==========================

If your custom HDF5 writer must create a group and you are uncertain which base
class to select, it is recommended to use the **NXnote** [#NXnote]_ base
class.

If your data does not fit the structure of the **NXnote** base class,
you are encouraged to find one of the other NeXus base classes that
best fits your data.  Look at the source code of the supplied plugins
for examples.

As a last resort, if your content cannot fit within the parameters of the NeXus
standard, use **NXcollection**, [#NXcollection]_ an unvalidated catch-all base
class) which can store any content.

The writer uses the :mod:`~spec2nexus.eznx` module to create and write
the various parts of the HDF5 file.

Example ``writer()`` method
===========================

Here is an example :meth:`writer` method from the
:mod:`~spec2nexus.plugins.unicat` module:

.. code-block:: python
   :linenos:

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr(scan, 'metadata') and len(scan.metadata) > 0:
            desc='SPEC metadata (UNICAT-style #H & #V lines)'
            group = eznx.makeGroup(h5parent, 'metadata', nxclass, description=desc)
            writer.save_dict(group, scan.metadata)

..  from the source code

   queue this by calling::
   
      scan.addWriter('unique_label', self.writer)
   
   in the process() method.  It will be called
   called as the HDF5 file is being constructed.
   
   .. tip:  One suggestion for the unique label is ``self.key``.
   
   If this method is to be used, then override this method in the 
   plugin or a :class:`NotImplementedError` exception will be raised.

.. _custom_key_match_function:

Custom key match function
*************************

The default test that a given line
matches a specific :class:`spec2nexus.plugin_core.ControlLineBase` subclass
is to use a regular expression match.  

.. code-block:: python
   :linenos:

    def match_key(self, text):
        '''default regular expression match, based on self.key'''
        t = re.match(self.key, text)
        if t is not None:
            if t.regs[0][1] != 0:
                return True
        return False


In some cases, that may prove tedious or difficult, such as when testing for a
floating point number with optional preceding white space at the start of a
line.  This is typical for data lines in a scan or continued lines from an MCA
spectrum.  in such cases, the handler can override the :meth:`match_key()`
method.  Here is an example from
:class:`~spec2nexus.plugins.spec_common.SPEC_DataLine`:

.. code-block:: python
   :linenos:

    def match_key(self, text):
        '''
        Easier to try conversion to number than construct complicated regexp
        '''
        try:
            float( text.strip().split()[0] )
            return True
        except ValueError:
            return False


.. _howto_summary_requirements:

Summary Requirements for custom plugin
**************************************

* file can go in any directory
* directory containing does not need a ``__init__.py`` file
* multiple control line handlers (plugins) can go in a single file
* for each control line:

  * subclass :class:`~spec2nexus.plugin_core.ControlLineBase`
  * identify the control line pattern
  * define ``key`` with a regular expression to match [#]_
  
    * ``key`` is used to identify control line handlers
    * redefine existing supported :index:`control line` control lines to replace supplied behavior (use caution!)
    * Note: ``key="scan data"`` is used to process the scan data:
      :meth:`~spec2nexus.plugins.spec_common.SPEC_DataLine`
  
  * define a ``process()`` method to handle the supplied text
  * (optional) define a ``postprocess()`` method to coordinate data from several ``process()`` steps
  * define a ``writer()`` method to write the in-memory data structure from this plugin to HDF5+NeXus data file
  * (optional) define :meth:`match_key` to override the default regular expression to match the key

* for each postprocessing method:

  * write the method
  * register the method with ``spec_obj.addPostProcessor(key_name, the_method)``
    in the handler's :meth:`~spec2nexus.plugin_core.ControlLineBase.process()` method.

* for each plugin file you want to load:

  * call :func:`~spec2nexus.plugin_core.install_user_plugin()` with the absolute path to the file

----------

.. _howto_changes_plugin_2022_release:

Changes in plugin format with release 2021.2.0
**********************************************

* subclassing and installing is easier (no need for ``metaclass`` kwarg)

  * subclass from :class:`~spec2nexus.plugin_core.ControlLineBase`
  * call :func:`~spec2nexus.plugin_core.install_user_plugin()` to install

.. _howto_changes_plugin_2021_release:

Changes in plugin format with release 2021.0.0
**********************************************

With release *2021.0.0*, the code to setup plugins has changed. The new code
allows all plugins in a module to auto-register themselves *as long as the
module is imported*. **All** custom plugins must be modified and import code
revised to work with new system. See the :mod:`spec2nexus.plugins.spec_common`
source code for many examples.

* SAME: The basics of writing the plugins remains the same.
* CHANGED: The method of registering the plugins has changed.
* CHANGED: The declaration of each plugin has changed.
* CHANGED: The name of each plugin file has been relaxed.
* CHANGED: Plugin files do not have to be in their own directory.
* REMOVED: The ``SPEC2NEXUS_PLUGIN_PATH`` environment variable has been eliminated.

----------

.. _howto_footnotes:

Footnotes
*********

.. [#] The key name must be unique amongst all postprocessing functions.
   A good choice is the name of the postprocessing function itself.
.. [#] https://nexusformat.org
.. [#] https://download.nexusformat.org/doc/html/classes/base_classes/
.. [#] https://download.nexusformat.org/doc/html/classes/base_classes/NXentry.html
.. [#NXnote] https://download.nexusformat.org/doc/html/classes/base_classes/NXnote.html
.. [#NXcollection] https://download.nexusformat.org/doc/html/classes/base_classes/NXcollection.html
.. [#] It is possible to override the default regular expression match
   in the subclass with a custom match function.  See the
   :meth:`~spec2nexus.plugins.spec_common.SPEC_DataLine.match_key()`
   method for an example.
