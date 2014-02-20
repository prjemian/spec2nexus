#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


'''
(Easy NeXus) support reading & writing NeXus HDF5 files using h5py

:predecessor: NeXus h5py example code: ``my_lib.py`` [#]_

.. [#] http://download.nexusformat.org/doc/html/examples/h5py/index.html#mylib-support-module
'''


import h5py    # HDF5 support
#import numpy   # in this case, provides data structures


def makeFile(filename, **attr):
    """
    create and open an empty NeXus HDF5 file using h5py
    
    Any named parameters in the call to this method will be saved as
    attributes of the root of the file.
    Note that ``**attr`` is a dictionary of named parameters.

    :param str filename: valid file name
    :param attr: optional keywords of attributes
    :return: h5py file object
    """
    obj = h5py.File(filename, "w")
    addAttributes(obj, **attr)
    return obj


def makeGroup(parent, name, nxclass, **attr):
    """
    create a NeXus group
    
    Any named parameters in the call to this method 
    will be saved as attributes of the group.
    Note that ``**attr`` is a dictionary of named parameters.
    
    :param obj parent: parent group
    :param str name: valid NeXus group name
    :param str nxclass: valid NeXus class name
    :param attr: optional keywords of attributes
    :return: h5py group object

    """
    obj = parent.create_group(name)
    obj.attrs["NX_class"] = nxclass
    addAttributes(obj, **attr)
    return obj


def makeDataset(parent, name, data = None, **attr):
    '''
    create and write data to a dataset in the HDF5 file hierarchy
    
    Any named parameters in the call to this method 
	will be saved as attributes of the dataset.

    :param obj parent: parent group
    :param str name: valid NeXus dataset name
    :param obj data: the data to be saved
    :param attr: optional keywords of attributes
    :return: h5py dataset object
    '''
    if data == None:
        obj = parent.create_dataset(name)
    else:
        obj = parent.create_dataset(name, data=data)
    addAttributes(obj, **attr)
    return obj


def makeLink(parent, sourceObject, targetName):
    """
    create an internal NeXus (hard) link in an HDF5 file

    :param obj parent: parent group of source
    :param obj sourceObject: existing HDF5 object
    :param str targetName: HDF5 node path to be created, 
                            such as ``/entry/data/data``
    """
    if not 'target' in sourceObject.attrs:
        # NeXus link, NOT an HDF5 link!
        sourceObject.attrs["target"] = str(sourceObject.name)
    import h5py.h5g
    parent._id.link(sourceObject.name, targetName, h5py.h5g.LINK_HARD)


def makeExternalLink(hdf5FileObject, sourceFile, sourcePath, targetPath):
    """
    create an external link from sourceFile, sourcePath to targetPath in hdf5FileObject

    :param obj hdf5FileObject: open HDF5 file object
    :param str sourceFile: file containing existing HDF5 object at sourcePath
    :param str sourcePath: path to existing HDF5 object in sourceFile
    :param str targetPath: full node path to be created in current open HDF5 file, 
                            such as ``/entry/data/data``
                            
    .. note::
       Since the object retrieved is in a different file, 
       its ".file" and ".parent" properties will refer to 
       objects in that file, not the file in which the link resides.

    :see: http://www.h5py.org/docs-1.3/guide/group.html#external-links
    
    This routine is provided as a reminder how to do this simple operation.
    """
    hdf5FileObject[targetPath] = h5py.ExternalLink(sourceFile, sourcePath)


def addAttributes(parent, **attr):
    """
    add attributes to an h5py data item

    :param obj parent: h5py parent object
    :param dict attr: dictionary of attributes
    """
    if attr and type(attr) == type({}):
        # attr is a dictionary of attributes
        for k, v in attr.items():
            parent.attrs[k] = v
