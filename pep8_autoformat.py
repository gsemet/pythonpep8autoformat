# -*- coding: utf-8 -*-

# Copyright 2012 Stéphane Bunel
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

import copy
import sys
import os
import sublime
import sublime_plugin

settings = sublime.load_settings('pep8_autoformat.sublime-settings')
IGNORE = ','.join(settings.get('ignore', []))
SELECT = ','.join(settings.get('select', []))
MAX_LINE_LENGTH = settings.get('max-line-length', 79)

pkg_path = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(pkg_path, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
(sys.path.insert(0, p) for p in settings.get('libs_path', []) if p not in sys.path)

try:
    import autopep8
except:
    sublime.error_message('Cannot import pep8 or autopep8!\n{0}'.format(sys.exc_info[1]))
    raise


class Pep8AutoformatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        source = ''
        replace_region = None
        pos = None
        sel = self.view.sel()

        if len(sel) > 1:
            sublime.error_message(
                'Python PEP8 Autoformat cannot work with multi selection')
            return
        elif len(sel) == 1:
            region = sel[0]
            if region.empty():  # Get all document
                pos = region.begin()
                replace_region = self.view.line(sublime.Region(0L, self.view.size()))
            else:
                replace_region = self.view.line(sel[0])

            scope = self.view.syntax_name(replace_region.end())
            if scope.find('source.python') == -1:
                sublime.error_message(
                    'Python PEP8 Autoformat apply only on Python code.\n'
                    'Current scope is: \"{0}\"'.format(scope))
                return

            source = self.view.substr(replace_region)
        else:
            return

        #-- Autoformat
        class options(object):
            def __init__(self):
                self.ignore = IGNORE
                self.select = SELECT
                self.verbose = False
                self.max_line_length = MAX_LINE_LENGTH

        refix = True
        while refix:
            fix = autopep8.FixPEP8(None, options(), contents=source)
            fixed = fix.fix()  # -- does not alway return Unicode string !
            #-- seems no more necessary with autopep8 commit 524505845cf72c2b5a072e7f2fdc7a0824ada12a
            if isinstance(fixed, str):
                fixed = fixed.decode('utf-8')
            if fixed == source:
                refix = False
            else:
                source = copy.copy(fixed)

        self.view.replace(edit, replace_region, source)

        if pos:
            self.view.sel().clear()
            self.view.sel().add(pos)
            self.view.show_at_center(pos)


class Pep8AutoformatBackground(sublime_plugin.EventListener):

    def on_post_save(self, view):
        syntax = view.settings().get('syntax')
        if syntax.find('Python.tmLanguage') == -1:
            return

        # do autoformat on file save if allowed in settings
        if settings.get('autoformat_on_save', False):
            view.run_command('pep8_autoformat')
