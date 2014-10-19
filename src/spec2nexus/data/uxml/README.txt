.. restructured text format

About test_1.spec
-----------------

This file is from Christian Schleputz and is an example file
written with his new way of storing metadata in the scan header
using XML.

:file:     		**test_1.spec**
:type:			SPEC scans
:description:	1-D scans, test file with #UXML lines in scan headers.
:date:			2014-09-29

..
	Thank you for the feedback! I have slightly modified the macros to incorporate some of the suggestions you made (see attached spec file with new version of metadata). The most important changes are:
	
	* removal of the type="str" attribute, as we will declare this the default in analogy to NeXus.
	* moved more information into an element's attributes list rather than keeping them in fields. There are two considerations here: (a) if it is defined as a field in any of the NeXus base classes, it will be a field in XML. The same goes for attributes. For things that are not defined in NeXus, I tried to make the following distinction: If a value is a description of the element, it should be added as an attribute. If the value contains "data" belonging to the element, it should go into a separate field. Typically, descriptions should be rather static (attributes), while the data (fields) is likely to change for every instance when we write the XML line.
	
	Let me know if there are any other issues. I would like to deploy these macros before the beginning of the cycle and have this be our new standard way of writing metadata into SPEC files as of the beginning of FY2015 or run 2014-3.
