#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
define the plug-in architecture
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


import os                           #@UnusedImport
import sys                          #@UnusedImport
import imp                          #@UnusedImport
import inspect                      #@UnusedImport
import pprint                       #@UnusedImport
import re                           #@UnusedImport
from pySpec import strip_first_word


PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE = 'SPEC2NEXUS_PLUGIN_PATH'
PLUGIN_INTERNAL_SUBDIRECTORY = 'control_lines'
PATH_DELIMITER = ','
FILE_NAME_ENDING = '_handlers.py'


class DuplicateControlLineKey(Exception): 
    '''This control line key regular expression has been used more than once.'''
    pass


class DuplicatePlugin(Exception): 
    '''This plugin file name has been used more than once.'''
    pass


class ControlLineHandler(object):
    '''
    Handle a single control line in a SPEC data file
    
    Create a subclass of ControlLineHandler for each different control line.
    
    * The subclass must define a value for the ``key_regexp`` which is
      unique across all :class:`ControlLineHandler` classes.
    * The subclass must override the definition of :meth:`process` and
      return either None or a ??? dictionary ???
      # TODO: decide the return API for process()
    
    :param str key_regexp: regular expression to match a control line key, up to the first space
    '''
    
    key_regexp = None
    
    def getKey(self):
        return str(self.key_regexp)
    
    def __str__(self):
        return str(self.__name__)
    
    def process(self, *args, **kw):
        raise NotImplementedError       # MUST implement in the subclass


class ControlLineHandlerManager(object):
    '''
    Manage the set of SPEC data file control line plugins
    '''
    
    def __init__(self):
        self.handler_dict = {}
    
    def register(self, handler):
        '''add this handler to the list of known handlers, key must be unique'''
        handler_key = handler().getKey()
        if handler_key in self.handler_dict:
            raise DuplicateControlLineKey(handler_key)
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
        txt = spec_data_file_line[:pos]
        for key in self.handler_dict.keys():
            if re.match(key, txt) is not None:
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
        plugin_dict = self._identify_control_line_plugins(control_line_search_path)
        for _, v in plugin_dict.items():
            self.register(v)
    
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
            control_line_search_path += map(cleanup_name, search_path.split(PATH_DELIMITER))
        return control_line_search_path
    
    def _identify_control_line_plugins(self, plugin_path_list):
        '''
        build dictionary of plugin classes, keyed by control line
        '''
        control_line_dict = {}
        module_dict = self._getPluginFiles(plugin_path_list)
        def isControlLineHandler(obj):
            def cname(thing):
                return str(thing.__name__)
            return 'ControlLineHandler' in map(cname, inspect.getmro(obj))
        for k, v in module_dict.items():
            module_obj = imp.load_source(k, v)
            try:
                member_list = inspect.getmembers(module_obj)
                for k, class_obj in member_list:
                    if not inspect.isclass(class_obj):
                        continue
                    if not isControlLineHandler(class_obj):
                        continue
                    if k is 'ControlLineHandler':
                        continue
                    control_line = class_obj().getKey()
                    if control_line in control_line_dict:
                        raise DuplicateControlLineKey(control_line + ' in ' + v)
                    control_line_dict[control_line] = class_obj
            except AttributeError:
                pass
        return control_line_dict

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


def simple_test():
    os.environ[PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE] = 'C://Users//Pete//Desktop, /tmp'
    manager = ControlLineHandlerManager()
    manager.load_plugins()
    pprint.pprint(manager.handler_dict)

    spec_data = '''
        #S 1 ascan eta 43.6355 44.0355 40 1
        #D Thu Jul 17 02:38:24 2003
        #T 1 (seconds)
        #G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0 0 1 0 0 0 0
        #V110 101.701 56 1 4 1 1 1 1 992.253
        #@CHANN 1201 1110 1200 1
        #N 14
        #L eta H K L elastic Kalpha Epoch seconds signal I00 harmonic signal2 I0 I0
        #@MCA 16C
        #@CHANN 1201 1110 1200 1
        #o0 un0 mx my waxsx ax un5 az un7
        @A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
        #H4 FB_o2_on FB_o2_r FB_o2_sp
        #Pete wrote this stuff
        43.6835 0.998671 -0.0100246 11.0078 1 0 66 1 0 863 0 0 1225 1225
    '''
    for spec_line in spec_data.strip().splitlines():
        txt = spec_line.strip()
        if len(txt) > 0:
            key = manager.getKey(txt)
            print key, manager.get(key)

if __name__ == '__main__':
    simple_test()
