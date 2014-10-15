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


PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE = 'PRJPYSPEC_PLUGIN_PATH'


class ControlLineHandler(object):
    '''
    Handle a single control line in a SPEC data file
    
    Create a subclass of ControlLineHandler for each different control line
    '''
    
    plugin_name = None
    
    def getName(self):
        return str(self.plugin_name)
    
    def __str__(self):
        return str(self.__name__)


class ControlLineHandlerManager(object):
    '''
    Manage the set of SPEC data file control line plugins
    '''
    
    def __init__(self):
        self.handler_dict = {}
    
    def register(self, handler):
        handler_name = handler().getName()
        if handler_name not in self.handler_dict:
            self.handler_dict[handler_name] = handler
        # TODO: else report warning that handler was already known


def getPluginFiles(plugin_path_list):
    '''
    construct a dictionary of modules containing plugin classes, keyed by module name
    '''
    match_key = '_handlers.py'
    module_dict = {}
    for path in plugin_path_list:
        if not os.path.exists(path):
            continue
        for fname in os.listdir(path):
            full_name = os.path.join(path, fname)
            if not os.path.isfile(full_name):
                continue
            if not fname.endswith(match_key):
                continue
            module_name = os.path.splitext(fname)[0]
            if module_name not in module_dict:
                module_dict[module_name] = full_name
            # TODO: else report warning that module_name was already known
    return module_dict


def identify_control_line_plugins(plugin_path_list):
    '''
    construct a dictionary of plugin classes, keyed by control line
    '''
    control_line_dict = {}
    module_dict = getPluginFiles(plugin_path_list)
    def isControlLineHandler(obj):
        def cname(thing):
            return str(thing.__name__)
        return 'ControlLineHandler' in map(cname, inspect.getmro(obj))
    for k, v in module_dict.items():
        module_obj = imp.load_source(k, v)
        try:
            member_list = inspect.getmembers(module_obj)
            for k, obj in member_list:
                if not inspect.isclass(obj):
                    continue
                if not isControlLineHandler(obj):
                    continue
                if k is 'ControlLineHandler':
                    continue
                control_line = obj.plugin_name
                if control_line not in control_line_dict:
                    control_line_dict[control_line] = obj
                # TODO: else report warning that control line was already known
        except AttributeError:
            pass
    return control_line_dict


def getSearchPath(internal_path, env_var_name):
    '''
    construct the list of directories in which Control Line plugins may be found
    '''
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), internal_path)
    control_line_search_path = [path, ]
    search_path = os.environ.get(env_var_name, None)
    def cleanup_name(txt):
        return txt.strip()
    if search_path is not None:
        control_line_search_path += map(cleanup_name, search_path.split(','))
    return control_line_search_path


if __name__ == '__main__':
    os.environ[PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE] = 'C://Users//Pete//Desktop, /tmp'
    control_line_search_path = getSearchPath('control_lines', PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE)
    plugin_dict = identify_control_line_plugins(control_line_search_path)
    manager = ControlLineHandlerManager()
    for k, v in plugin_dict.items():
        manager.register(v)
    pprint.pprint(manager.handler_dict)
