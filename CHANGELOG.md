# CHANGELOG
Python PEP8 Autoformat

## 2012.07.19-1
- FIX: Restore caret position after reformatting the whole document.
- NEW: This file (CHANGELOG.md).

## 2012.07.18-1
- ADD: `Default.sublime-commands` file to call "Python PEP8 Autoformat" from Command Panel.
- ADD: `pep8_autoformat.sublime-settings` settings file:

		{
			// autoformat code on save ?
			"autoformat_on_save": false,

		    // autopep8 command path
		    "command": "autopep8",

		    // select errors / warnings(e.g. ["E4", "W"])
		    "select": [],

		    // do not fix these errors / warnings(e.g. ["E4", "W"])
		    "ignore": ["E501"],

		    // for debugging purpose (print executed command in console)
		    "show_command": false
		}

## 2012.07.17-1
- Source code published on [bitbucket](https://bitbucket.org/StephaneBunel/pythonpep8autoformat).

## 2012.07.15-1
- Learning how to create a plug-in for Sublime text 2,
- and write the first lines of code.
