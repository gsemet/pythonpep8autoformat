# -*- coding: utf-8 -*-

# Copyright 2012-2013 Stéphane Bunel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import os
import sublime
import sublime_plugin
import sys

PPA_PATH = list()
PYMAMI = '{0}{1}'.format(*sys.version_info[:2])
ST_VERSION = 3000 if sublime.version() == '' else int(sublime.version())
PLUGIN_NAME = "Python PEP8 Autoformat"
SETTINGS_FILE = 'pep8_autoformat.sublime-settings'

#-- Cannot use sublime.packages_path() with ST3 because of inconsistency
#-- of returned path between bootstap time vs running time.
#pkg_path = os.path.join(sublime.packages_path(), PLUGIN_NAME)
pkg_path = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(pkg_path, 'libs')
PPA_PATH.append(libs_path)

versionlibs_path = os.path.join(pkg_path, 'libs', 'py' + PYMAMI)
if os.path.exists(versionlibs_path):
    PPA_PATH.append(versionlibs_path)

print('Included directory to sys.path :', PPA_PATH)
[sys.path.insert(0, p) for p in PPA_PATH if p not in sys.path]

try:
    import autopep8
    import MergeUtils
except:
    sublime.error_message(
        '{0}: import error: {1}'.format(PLUGIN_NAME, sys.exc_info()[1]))
    raise

override_enable_python_autopep8 = None
disable_python_autopep8_for_files = set()
enable_python_autopep8_for_files = set()

def get_current_filename():
    view = sublime.Window.active_view(sublime.active_window())
    return os.path.abspath(view.file_name())


class EnablePythonAutopep8Command(sublime_plugin.TextCommand):

    def run(self, edit):
        global override_enable_python_autopep8
        printDebug("EnablePythonAutopep8Command")
        override_enable_python_autopep8 = True


class DisablePythonAutopep8Command(sublime_plugin.TextCommand):

    def run(self, edit):
        global override_enable_python_autopep8
        printDebug("DisablePythonAutopep8Command")
        override_enable_python_autopep8 = False


class DisablePythonAutopep8ForFileCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global disable_python_autopep8_for_files
        printDebug("DisablePythonAutopep8ForFileCommand")
        f = get_current_filename()
        disable_python_autopep8_for_files.add(f)
        if f in enable_python_autopep8_for_files:
            enable_python_autopep8_for_files.remove(f)


class EnablePythonAutopep8ForFileCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global enable_python_autopep8_for_files
        global disable_python_fiximports_for_file
        printDebug("enable_python_autopep8_for_files")
        f = get_current_filename()
        enable_python_autopep8_for_files.add(f)
        if f in disable_python_autopep8_for_files:
            disable_python_autopep8_for_files.remove(f)


class PythonPEP8Autoformat(object):

    def __init__(self):
        self.settings = sublime.load_settings(SETTINGS_FILE)

    def get_options(self):
        cmd_args = list()
        cmd_args.extend(['--aggressive'] * self.settings.get('aggressive', 0))
        if self.settings.get('list-fixes', False):
            cmd_args.append('--list-fixes')
        if self.settings.get('ignore', False):
            cmd_args.append('--ignore={0}'.format(','.join(
                [o.strip() for o in self.settings.get('ignore') if o.strip()])))
        if self.settings.get('select', False):
            cmd_args.append('--select={0}'.format(','.join(
                [o.strip() for o in self.settings.get('select') if o.strip()])))
        if self.settings.get('max-line-length', False):
            cmd_args.append('--max-line-length={0}'.format(
                self.settings.get('max-line-length')))
        if self.settings.get('indent-size', False):
            cmd_args.append('--indent-size={0}'.format(
                self.settings.get('indent-size')))
        #-- We must give a filename to pass the parse_args() tests
        cmd_args.append('filename')
        options = autopep8.parse_args(cmd_args)

        return options


class Pep8AutoformatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        syntax = self.view.settings().get('syntax')
        if syntax.lower().find('python') == -1:
            return
        replace_region = self.view.line(
            sublime.Region(0, self.view.size()))
        source = self.view.substr(replace_region)
        fixed = autopep8.fix_code(source, options=PPA.get_options())
        is_dirty, err = MergeUtils.merge_code(self.view, edit, source, fixed)
        if err:
            sublime.error_message(
                "%s: Merge failure: '%s'" % (PLUGIN_NAME, err))
            raise


class Pep8AutoformatBackground(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        syntax = view.settings().get('syntax')
        if syntax.lower().find('python') == -1:
            return

        # do autoformat on file save if allowed in settings
        if not PPA.settings.get('autoformat_on_save', False):
            return

        f = get_current_filename()

        if f in enable_python_autopep8_for_files:
            printDebug("Current file in list of forced AutoPep8. Do AutoPep8")
            view.run_command('pep8_autoformat')
            return

        if f in disable_python_autopep8_for_files:
            printDebug("Current file in list of disabled AutoPep8. Don't AutoPep8")
            return

        if override_enable_python_autopep8 is False:
            printDebug("Temporary override of AutoPep8 import set to Disabled. Do not AutoPep8")
            return

        view.run_command('pep8_autoformat')


# In ST3 this will get called automatically once
# the full API becomes available.
def plugin_loaded():
    global PPA
    PPA = PythonPEP8Autoformat()

if ST_VERSION < 3000:
    global PPA
    PPA = PythonPEP8Autoformat()
