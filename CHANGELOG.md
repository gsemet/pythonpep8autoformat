# CHANGELOG
Python PEP8 Autoformat

## 2012.09.10-1
- FIX: Enhance python code recognition

## 2012.09.07-1
- autopep8 updated to version 0.8

## 2012.08.02-1
- Python PEP8 Autoformat is now installable via [Sublime Package Control](http://wbond.net/sublime_packages/package_control)

## 2012.07.22-1
- Cosmetic code changes
- Tested under Windows 7
- Cleanup README.md (thanks to Georges Goncalves)

## 2012.07.21-2
- README update

## 2012.07.21-2
- FIX: OSX key binding is now `ctrl+shift+r`

## 2012.07.21-1
- NEW: Settings menu (Preferences -> Packages Settings -> Python PEP8 Autoformat)
- NEW: Include pep8 v1.3.3 and autopep8 v0.7.2 (with minor modifications) to remove all dependencies.
- FIX: variable reference

## 2012.07.19-1
- FIX: Restore caret position after reformatting the whole document.
- NEW: This file (CHANGELOG.md).

## 2012.07.18-1
- ADD: `Default.sublime-commands` file to call "Python PEP8 Autoformat" from Command Panel.
- ADD: `pep8_autoformat.sublime-settings` settings file:

		{
			// autoformat code on save ?
			"autoformat_on_save": false,

		    // path to autopep8 or "" to use packaged version
		    "command": "",

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
