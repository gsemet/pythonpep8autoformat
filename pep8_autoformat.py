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

import sys
import os
import subprocess
import tempfile
import sublime
import sublime_plugin

try:
    import autopep8
except:
    sublime.error_message('Cannot import autopep8!\n{0}'.format(sys.exc_info[1]))
    raise

settings = sublime.load_settings('pep8_autoformat.sublime-settings')
IGNORE = ','.join(settings.get('ignore', []))
SELECT = ','.join(settings.get('select', []))
AUTOPEP8 = settings.get('command', '')

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)
libs_path = os.path.join(__path__, 'libs')

if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
    
LIBS_PATH = settings.get('libs_path', [])

for lib_path in LIBS_PATH:
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)

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

        #-- Open tmpfile
        source_file = tempfile.NamedTemporaryFile(delete=False)

        #-- Write code to tmpfile
        source_file.write(source.encode('utf-8'))

        fname = source_file.name
        source_file.close()

        #-- Autoformat
        if AUTOPEP8 == '':
            class options(object):
                def __init__(self):
                    self.ignore = IGNORE
                    self.select = SELECT
                    self.verbose = False

            fix = autopep8.FixPEP8(source_file, options(), source.encode('utf-8'))
            self.view.replace(edit, replace_region, fix.fix().decode('utf-8'))
        else:
            cmd = [AUTOPEP8, "--in-place"]
            if IGNORE:
                cmd.append('--ignore')
                cmd.append(IGNORE)
            if SELECT:
                cmd.append('--select')
                cmd.append(SELECT)
            cmd.append(fname)
            if settings.get("show_command"):
                print('cmd="{0}"'.format(' '.join(cmd)))

            try:
                subprocess.call(cmd)
                with file(fname, 'rb') as f:
                    output = f.read().decode('utf-8')
                self.view.replace(edit, replace_region, output)
            except OSError as e:
                if e.errno == 2:
                    msg = '"{0}" not found !\n' \
                        'Set "command" path in Python PEP8 Autoformat settings.\n' \
                        'See https://github.com/hhatto/autopep8#installation if autopep8 is not installed'.format(
                        AUTOPEP8)
                else:
                    msg = e.message
                sublime.error_message(msg)
            except:
                sublime.error_message(str(sys.exc_info()[1]))

        #-- Remove tempfile
        try:
            os.unlink(fname)
        except:
            sublime.error_message(str(sys.exc_info()[1]))

        if pos:
            self.view.sel().clear()
            self.view.sel().add(pos)
            self.view.show_at_center(pos)


class Pep8AutoformatBackground(sublime_plugin.EventListener):

    def on_post_save(self, view):
        syntax = view.settings().get('syntax')
        if not syntax.endswith('Python.tmLanguage'):
            return

        # do autoformat on file save if allowed in settings
        if settings.get('autoformat_on_save', False):
            view.run_command('pep8_autoformat')
