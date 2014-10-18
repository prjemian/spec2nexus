
:mod:`spec2nexus.plugin`
########################

An extensible plug-in architecture is used to handle the different possible
control lines (such as **#F**, **#E**, **#S**, ...) in a SPEC data file.

Plugins can be used to parse or ignore certain control lines in SPEC data files.
Through this architecture, it is possible to support custom control lines, 
such as **#U** (SPEC standard control line for any user data).
One example is support for the :ref:`UNICAT-style <unicat_plugin>` of metadata 
provided in the scan header.

Plugins are now used to handle all control lines in :mod:`spec2nexus.pySpec`.
Any control line encountered but not recognized will raise a
:class:`~spec2nexus.pySpec.UnknownSpecFilePart` exception.


.. _supplied_plugins:

Summary of the supplied pySpec plugins
======================================

Plugins for these control lines [#]_ are provided in **spec2nexus**:

.. autosummary::
   :nosignatures:

   ~spec2nexus.control_lines.spec_common_handlers.SPEC_File
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Epoch
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Date
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Comment
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Geometry
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_NormalizingFactor
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_CounterNames
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_CounterMnemonics
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Labels
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Monitor
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_NumColumns
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_PositionerNames
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_PositionerMnemonics
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Positioners
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_HKL
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_Scan
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_CountTime
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_TemperatureSetPoint
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_DataLine
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_MCA
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_MCA_Array
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_MCA_Calibration
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_MCA_ChannelInformation
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_MCA_CountTime
   ~spec2nexus.control_lines.spec_common_handlers.SPEC_MCA_RegionOfInterest
   ~spec2nexus.control_lines.unicat_handlers.UNICAT_MetadataMnemonics
   ~spec2nexus.control_lines.unicat_handlers.UNICAT_MetadataValues
   ~spec2nexus.control_lines.uim_handlers.UIM_generic

.. [#] Compare this list with :ref:`control_line_list`

How to write a custom plugin module
===================================

.. sidebar:: Do not redefine control line plugins!

   Clearly stated, do not try to replace the standard handler for 
   **#S** (or other control lines) with your own handlers.

A custom plugin module for :mod:`spec2nexus.pySpec` is provided in a python module (Python source code file).
In this custom plugin module are subclasses for each *new* control line to be supported.  An exception will 
be raised if a custom plugin module tries to provide support for an existing control line.  

Give the custom plugin module a name ending with ``_handlers.py``.
Ensure this name is different than any other plugin module you will use
(currently, avoid ``spec_common_handlers.py``, ``uim_handlers.py``, 
and ``unicat_handlers.py``) to avoid possible duplication.

The custom plugin module can be stored in any directory that is convenient.
Define the environment variable ``SPEC2NEXUS_PLUGIN_PATH`` with the
directory (directories, comma delimited) where your plugin file(s) reside.
On linux, with the bash shell, this might be::

    export SPEC2NEXUS_PLUGIN_PATH="/home/jemian/.pySpec_plugins, /tmp"

The custom plugin module should contain, at minimum one subclass of  
:class:`spec2nexus.plugin.ControlLineHandler`.  A custom plugin module
can contain many such handlers, as needs dictate.

.. note::  It is also useful to import the utility method
   :meth:`spec2nexus.plugin.strip_first_word`

To get :class:`spec2nexus.plugin.ControlLineHandler`,
it will be necessary to import in some form, such as::

   from spec2nexus.plugin import ControlLineHandler, strip_first_word

.. sidebar:: regular expressions

   There are several regular expression testers available on the web.
   Try this one, for example: http://regexpal.com/

Each subclass must define ``key`` as a regular expression match for the 
control line key.  It is possible to override any of the supplied plugins.
Caution is advised to avoid introducing instability.

.. A :class:`~spec2nexus.plugin.DuplicateControlLineKey` 
   exception is raised if ``key`` is not defined.

Each subclass must also define a :meth:`process` method to process the control line.
A :class:`NotImplementedError` exception is raised if ``key`` is not defined.

Example for **#U** control line
-------------------------------

Consider the **#U** user data control line that allows the user to
put any data in the scan file header.  The content is to be decided 
by the user.

Suppose we take this content to be three floating 
point numbers, this subclass could be written::

   from spec2nexus.plugin import ControlLineHandler, strip_first_word
   
   class User_ControlLine(ControlLineHandler):
       '''**#U** -- User data (#U user1 user2 user3)'''
   
       key = '#U'
       
       def process(self, text, spec_obj, *args, **kws):
           args = strip_first_word(text).split()
           user1 = float(args[0])
           user2 = float(args[1])
           user3 = float(args[2])
           spec_obj.U = [user1, user2, user3]

When the scan parser encounters a **#U** line in a SPEC data file, it will call this
:meth:`process()` code with the full text of the line and the object where this data 
should be stored.  We will choose to store this (following the pattern of other data 
names in :class:`spec2nexus.pySpec.SpecDataFileScan`) as ``scan_obj.U`` using a list.

It is up to the user what to do with the ``scan_obj.U`` data.

Example to ignore a **#Y** control line
---------------------------------------

Suppose it is necessary to ignore a control line found in a SPEC file.
Consider that one SPEC file contains the control line: ``#Y 1 2 3 4 5``.
Since there is no standard handler for this control line, we create one that
ignores processing by doing nothing::

   from spec2nexus.plugin import ControlLineHandler
   
   class Ignore_Y_ControlLine(ControlLineHandler):
       '''**#Y** -- as in ``#Y 1 2 3 4 5``'''
   
       key = '#Y'
       
       def process(self, text, spec_obj, *args, **kws):
           pass

Postprocessing
--------------

Sometimes, it is necessary to defer a step of processing until after the complete
scan data has been read.  One example if for 2-D or 3-D data that has been acquired
as a vector rather than matrix.  The matrix must be constructed only after all the 
scan data has been read.  Such postprocessing is handled in a method in a plugin file.
The postprocessing method is registered from the control line handler by calling the
:meth:`addPostProcessor` method of the ``spec_obj`` argument received by the 
handler's :meth:`process` method.  A key name [#]_ is supplied when registering to avoid 
registering this same code more than once.  The postprocessing function will be called 
with the instance of :class:`spec2nexus.pySpec.SpecDataFileScan` as its only argument.

.. [#] The key name must be unique amongst all postprocessing functions.
   A good choice is the name of the postprocessing function itself.
   

Example postprocessing
++++++++++++++++++++++

Consider the **#U** control line example above.  For some contrived reason,
we wish to store the sum of the numbers as a separate number, but only after 
all the scan data has been read.  This can be done with the simple expression::

   spec_obj.U_sum = sum(spec_obj.U)

To build a postprocessing method, we write::

   def contrived_summation(scan):
       '''
       add up all the numbers in the #U line
       
       :param SpecDataFileScan scan: data from a single SPEC scan
       '''
       scan.U_sum = sum(scan.U)

To register this postprocessing method, place this line in the :meth:`process`
of the handler::

   spec_obj.addPostProcessor('contrived_summation', contrived_summation)

Summary Example Custom Plugin with postprocessing
+++++++++++++++++++++++++++++++++++++++++++++++++

Gathering all parts of the examples above, the custom plugin module is::

   from spec2nexus.plugin import ControlLineHandler, strip_first_word
   
   class User_ControlLine(ControlLineHandler):
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
   
   
   class Ignore_Y_ControlLine(ControlLineHandler):
       '''**#Y** -- as in ``#Y 1 2 3 4 5``'''
   
       key = '#Y'
       
       def process(self, text, spec_obj, *args, **kws):
           pass

Custom key match function
-------------------------

The default test that a given line
matches a specific :class:`spec2nexus.plugin.ControlLineHandler` subclass
is to use a regular expression match.  

::

    def match_key(self, text):
        '''default regular expression match, based on self.key'''
        t = re.match(self.key, text)
        if t is not None:
            if t.regs[0][1] != 0:
                return True
        return False


In some cases, that may
prove tedious or difficult, such as when testing for a
floating point number with optional preceding white space
at the start of a line.  This is typical for data lines in a scan
or continued lines from an MCA spectrum.  in such cases, the handler
can override the :meth:`match_key()` method.  Here is an example::

    def match_key(self, text):
        '''
        Easier to try conversion to number than construct complicated regexp
        '''
        try:
            float( text.strip().split()[0] )
            return True
        except ValueError:
            return False


Summary Requirements for custom plugin
--------------------------------------

* file name must end in ``_handlers.py``
* file can go in any directory
* add directory to ``SPEC2NEXUS_PLUGIN_PATH`` environment variable (comma-delimited for multiple directories)
* multiple control line handlers can go in a single file
* for each control line:

  * do not redefine existing supported control lines
  * subclass :class:`spec2nexus.plugin.ControlLineHandler`
  * identify the control line pattern
  * define ``key`` with a regular expression to match [#]_
  * define :meth:`process` to handle the supplied text

* for each postprocessing function:

  * write the function
  * register the function with spec_obj.addPostProcessor(key_name, the_function) in the handler's :meth:`process`

.. [#] It is possible to override the default regular expression match
   in the subclass with a custom match function.  See the
   :meth:`spec2nexus.control_lines.spec_common_handlers.SPEC_DataLine.match_key()`
   method for an example.

source code documentation
=========================

.. automodule:: spec2nexus.plugin
    :members: 
    :synopsis: Define the plug-in architecture.

supplied plugins
================

.. _spec_plugin:

SPEC standard plugin
--------------------

.. automodule:: spec2nexus.control_lines.spec_common_handlers
    :members: 
    :synopsis: SPEC standard data file support.

.. _unicat_plugin:

UNICAT metadata plugin
----------------------

.. automodule:: spec2nexus.control_lines.unicat_handlers
    :members: 
    :synopsis: Metadata in SPEC data files as defined by APS UNICAT.

.. _uim_plugin:

UIM plugin
----------

.. automodule:: spec2nexus.control_lines.uim_handlers
    :members: 
    :synopsis: Image header information from EPICS areaDetector.

