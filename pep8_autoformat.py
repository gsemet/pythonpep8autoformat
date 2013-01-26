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

import sys
import os
import sublime
import sublime_plugin

PLUGIN_NAME = "Python PEP8 Autoformat"
settings = sublime.load_settings('pep8_autoformat.sublime-settings')
IGNORE = ','.join(settings.get('ignore', []))
SELECT = ','.join(settings.get('select', []))
MAX_LINE_LENGTH = settings.get('max-line-length', 79)
AGGRESSIVE = settings.get('aggressive', False)

pkg_path = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(pkg_path, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
(sys.path.insert(0, p) for p in settings.get('libs_path', []) if p not in sys.path)

try:
    import autopep8
    import MergeUtils
except:
    sublime.error_message(
        '{0}: import error: {1}'.format(PLUGIN_NAME, sys.exc_info[1]))
    raise


class Pep8AutoformatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        source = ''
        replace_region = None
        sel = self.view.sel()

        if len(sel) > 1:
            sublime.error_message('Python PEP8 Autoformat cannot work with multi selection')
            return
        elif len(sel) == 1:
            region = sel[0]
            if region.empty():  # Get all document
                replace_region = self.view.line(
                    sublime.Region(0L, self.view.size()))
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

        options = autopep8.parse_args([''])[0]
        if IGNORE:
            options.ignore = IGNORE
        if SELECT:
            options.select = SELECT
        if MAX_LINE_LENGTH:
            options.max_line_length = MAX_LINE_LENGTH
        if AGGRESSIVE:
            options.aggressive = True

        fixed = autopep8.fix_string(source, options=options)
        is_dirty, err = MergeUtils.merge_code(self.view, edit, source, fixed)
        if err:
            sublime.error_message(
                "%s: Merge failure: '%s'" % (PLUGIN_NAME, err))


class Pep8AutoformatBackground(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        syntax = view.settings().get('syntax')
        if syntax.find('Python.tmLanguage') == -1:
            return

        # do autoformat on file save if allowed in settings
        if settings.get('autoformat_on_save', False):
            view.run_command('pep8_autoformat')
