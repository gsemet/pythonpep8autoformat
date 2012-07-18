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

#-- 2012-07-15, Stéphane Bunel
#--           * Learning how to create a plug-in for ST2
#--           * Write the first lines of code.
#-- 2012-07-17, Stéphane Bunel
#--           * Published on bitbucket.
#--           * Version 2012.07.17.19.01.55
#-- 2012-07-18, Stéphane Bunel
#--           * Add Default.sublime-commands file
#--           * Add 'show_command' setting
#--
#-- TODO:
#--           * How to restore cursor position after replace() ?

import sys
import os
import subprocess
import tempfile
import sublime
import sublime_plugin


settings = sublime.load_settings('pep8_autoformat.sublime-settings')
AUTOPEP8 = settings.get('command', 'autopep8')
IGNORE = ','.join(settings.get('ignore', []))
SELECT = ','.join(settings.get('select', []))


class Pep8AutoformatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        source = ''
        region = None
        sel = self.view.sel()
        syntax = self.view.settings().get('syntax')

        if not syntax.endswith('Python.tmLanguage'):
            sublime.error_message(
                'Not a Python syntax. Current is:\n{0}'.format(syntax))
            return

        if len(sel) > 1:
            sublime.error_message(
                'PythonFormat8 cannot works with multi selection')
            return
        elif len(sel) == 1:
            region = sel[0]
            if region.empty():
                #-- Get all document
                region = self.view.line(sublime.Region(0L, self.view.size()))
                source = self.view.substr(region)
            else:
                #-- Get selected code
                region = self.view.line(sel[0])
                source = self.view.substr(region)
        else:
            sublime.error_message('Hu! document with no selection !')
            return

        #-- Open tmpfile
        source_file = tempfile.NamedTemporaryFile(delete=False)

        #-- Write code to tmpfile
        source_file.write(source.encode('utf-8'))

        fname = source_file.name
        source_file.close()

        #-- Run autopep8 on tmpfile
        cmd = [AUTOPEP8, "--in-place"]
        if IGNORE:
            cmd.append('--ignore')
            cmd.append(IGNORE)
        if SELECT:
            cmd.append('--select')
            cmd.append(SELECT)
        cmd.append(fname)
        if settings.get("show_command"):
            print('cmd="{0}"'.format( ' '.join(cmd)))

        try:
            subprocess.call(cmd)
            output = file(fname, 'rb').read().decode('utf-8')
            self.view.replace(edit, region, output)
        except OSError as e:
            if e.errno == 2:
                msg = 'Command {0} not found\nSee https://github.com/hhatto/autopep8#installation for installation'.format(
                    self.AUTOPEP8)
            else:
                msg = e.message
            sublime.error_message(msg)
        except:
            sublime.error_message(str(sys.exc_info()[1]))

        #-- Remove tempfile
        os.unlink(fname)


class Pep8AutoformatBackground(sublime_plugin.EventListener):

    def on_post_save(self, view):
        syntax = view.settings().get('syntax')
        if not syntax.endswith('Python.tmLanguage'):
            return

        # do autoformat on file save if allowed in settings
        if settings.get('autoformat_on_save', False):
            view.run_command('pep8_autoformat')
