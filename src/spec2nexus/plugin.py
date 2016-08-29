#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

'''
define the plug-in architecture

Create a subclass of :class:`spec2nexus.plugin.ControlLineHandler`
for each SPEC control line.  In each subclass, it is necessary to:

* define a string value for the ``key`` (class attribute)
* override the definition of :meth:`process`

It is optional to:

* override the definition of :meth:`match_key`
* override the definition of :meth:`postprocess`
* override the definition of :meth:`writer`

'''


import os                           #@UnusedImport
import sys                          #@UnusedImport
import imp                          #@UnusedImport
import inspect                      #@UnusedImport
import pprint                       #@UnusedImport
import re                           #@UnusedImport
from spec2nexus.utils import strip_first_word #@UnusedImport


PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE = 'SPEC2NEXUS_PLUGIN_PATH'
PLUGIN_INTERNAL_SUBDIRECTORY = 'plugins'
PATH_DELIMITER = ','
FILE_NAME_ENDING = '_spec2nexus.py'


class DuplicateControlLinePlugin(Exception): 
    '''This control line handler has been used more than once.'''
    pass


class DuplicateControlLineKey(Exception): 
    '''This control line key regular expression has been used more than once.'''
    pass


class DuplicatePlugin(Exception): 
    '''This plugin file name has been used more than once.'''
    pass


class ControlLineHandler(object):
    '''
    Plugin to handle a single control line in a SPEC data file

    :param str key: regular expression to match a control line key, up to the first space
    :returns: None
    '''
    
    key = None
    
    def getKey(self):
        '''return this handler's unique identifying key'''
        return str(self.key)
    
    def match_key(self, text):
        '''
        test if this plugin's key matches the supplied text
        
        :param str text: first word on the line, 
            up to but not including the first whitespace
        
        The default test is to apply a regular expression match
        using ``self.key`` as the regular expression to match.

        If this method is to be used, then override this method in the 
        plugin or a :class:`NotImplementedError` exception will be raised.
        '''
        # ensure that #X and #XPCS do not both match #X
        full_pattern = '^' + self.key + '$'
        t = re.match(full_pattern, text)
        # test regexp match to avoid false positives
        # ensures that beginning and end are different positions
        return t and t.regs[0][1] != t.regs[0][0]

    def __str__(self):
        return str(self.__name__)
    
    def process(self, *args, **kw):
        '''
        Parse this text from the SPEC data file according to the control line key.
        
        A plugin will receive *text* and one of these objects: 
        * :class:`~spec2nexus.spec.SpecDataFile`
        * :class:`~spec2nexus.spec.SpecDataFileHeader`
        * :class:`~spec2nexus.spec.SpecDataFileScan`
        
        The plugin will parse the text and store the content into the object.

        All plugins **must** override this method 
        or a :class:`NotImplementedError` exception will be raised.
        '''
        
        raise NotImplementedError(self.__class__)       # MUST implement in the subclass
    
    def postprocess(self, *args, **kw):
        '''
        apply additional interpretation after all control lines have been read

        queue this method by calling::
        
            scan.addPostProcessor('unique label', self.postprocess)
        
        in the :meth:`process` method.  It will be called
        called after all control lines in a scan have been read.

        .. tip:  One suggestion for the unique label is ``self.key``.

        If this method is to be used, then override this method in the 
        plugin or a :class:`NotImplementedError` exception will be raised.
        '''
        
        raise NotImplementedError(self.__class__)       # MUST implement in the subclass
    
    def writer(self, *args, **kw):
        '''
        write in-memory structure to HDF5+NeXus data file
        
        queue this by calling::
        
            scan.addWriter('unique_label', self.writer)
        
        in the process() method.  It will be called
        called as the HDF5 file is being constructed.

        .. tip:  One suggestion for the unique label is ``self.key``.

        If this method is to be used, then override this method in the 
        plugin or a :class:`NotImplementedError` exception will be raised.
        '''
        
        raise NotImplementedError(self.__class__)       # MUST implement in the subclass


class PluginManager(object):
    '''
    Manage the set of SPEC data file control line plugins
    '''
    
    def __init__(self):
        self.handler_dict = {}
    
    def register(self, handler):
        '''add this handler to the list of known handlers'''
        handler_key = handler().getKey()
        if handler_key is None:
            raise NotImplementedError('Must define **key** in ' + self.__class__)
#         if handler_key in self.handler_dict:
#             raise DuplicateControlLineKey(handler_key)
        self.handler_dict[handler_key] = handler
    
    def hasKey(self, key):
        '''Is this key known?'''
        return key in self.handler_dict
    
    def getKey(self, spec_data_file_line):
        '''
        Find the key that matches this line in a SPEC data file.  Return None if not found.
        
        :param str spec_data_file_line: one line from a SPEC data file
        '''
        pos = spec_data_file_line.find(' ')
        if pos < 0:
            return None
        text = spec_data_file_line[:pos]
        for key, handler in self.handler_dict.items():
            if handler().match_key(text):
                return key
        return None

    def get(self, key):
        '''return the handler identified by key or None'''
        if not self.hasKey(key):
            return None
        return self.handler_dict[key]
    
    def load_plugins(self):
        '''
        Call this once to load all plugins that handle SPEC control lines
        '''
        env_var = PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE
        internal_dir = PLUGIN_INTERNAL_SUBDIRECTORY
        control_line_search_path = self._getSearchPath(internal_dir, env_var)
        self._register_control_line_plugins(control_line_search_path)
    
    def _getSearchPath(self, internal_path, env_var_name):
        '''
        construct the list of directories in which Control Line plugins may be found
        '''
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), internal_path)
        control_line_search_path = [path, ]
        search_path = os.environ.get(env_var_name, None)
        def cleanup_name(txt):
            return txt.strip()
        if search_path is not None:
            # ALWAYS add the custom search path AFTER the internal one
            control_line_search_path += map(cleanup_name, search_path.split(PATH_DELIMITER))
        return control_line_search_path
    
    def _register_control_line_plugins(self, plugin_path_list):
        '''
        register all plugin classes, keyed by control line key
        '''
        module_dict = self._getPluginFiles(plugin_path_list)
        def isControlLineHandler(obj):
            def cname(thing):
                return str(thing.__name__)
            return 'ControlLineHandler' in map(cname, inspect.getmro(obj))
        for k, v in module_dict.items():
            module_obj = imp.load_source(k, v)
            try:
                member_list = inspect.getmembers(module_obj)
                for kk, class_obj in member_list:
                    if not inspect.isclass(class_obj):
                        continue
                    if not isControlLineHandler(class_obj):
                        continue
                    if kk is 'ControlLineHandler':
                        continue
                    self.register(class_obj)
            except AttributeError:
                pass

    def _getPluginFiles(self, plugin_path_list):
        '''
        build dictionary of modules containing plugin classes, keyed by module name
        '''
        module_dict = {}
        for path in plugin_path_list:
            if not os.path.exists(path):
                continue
            for fname in os.listdir(path):
                full_name = os.path.join(path, fname)
                if not os.path.isfile(full_name):
                    continue
                if not fname.endswith(FILE_NAME_ENDING):
                    continue
                module_name = os.path.splitext(fname)[0]
                if module_name in module_dict:
                    raise DuplicatePlugin(module_name + ' in ' + full_name)
                module_dict[module_name] = full_name
        return module_dict
    
    def process(self, key, *args, **kw):
        '''pick the control line handler by key and call its process() method'''
        handler = self.get(key)
        if handler is not None:
            handler().process(*args, **kw)
