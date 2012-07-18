Two days ago, looking for an eventual Eclipse replacement, I started to use [Sublime Text 2](http://www.sublimetext.com/).
One of my main usages of PyDev (Python Eclipse plug-in) is the code formatter.
PythonTidy is a PEP8 code formatter plug-in for ST2. But unfortunately it did not work for me.
So, for fun and learning, I decided to create a new ST2 plugin: Python PEP8 Autoformat

# Python PEP8 Autoformat

Python PEP8 Autoformat is a Sublime Text 2 plug-in for reformat Python source code according to [PEP8](http://www.python.org/dev/peps/pep-0008/) (Style Guide for Python Code) using [autopep8](https://github.com/hhatto/autopep8) tool.

## Installation

**autopep8**

Before using Python PEP8 Autoformat you should [install](https://github.com/hhatto/autopep8#installation) `autopep8`.

**Python PEP8 Autoformat**

1. Via [Sublime Package Manager](http://wbond.net/sublime_packages/package_control)
    + Use `cmd+shift+P` then `Package Control: Install Package`
    + Look for `Python PEP8 Autoformat` and install it.

1. Via the repository and mercurial:
    + Open a terminal, cd to ST2/Packages directory (Preference -> Browse packages). Then type in terminal:
    + `hg clone https://bitbucket.org/StephaneBunel/pythonpep8autoformat 'Python PEP8 Autoformat'`

1. Manually:
    + Download an [archive](https://bitbucket.org/StephaneBunel/pythonpep8autoformat/downloads) of Python PEP8 Autoformat
    + Move into ST2/Packages directory (Preference -> Browse packages) and create a new directory named 'Python PEP8 Autoformat'
    + Extract archive contents into 'Python PEP8 Autoformat' directory.

## Usage

Your document must be set to use the Python syntax (default for all .py files).
When asked, the reformatting is applied on the whole code.
If you want to apply it on a subpart only, just select it before.

### Using keyboard:

- Linux:   `ctrl+shift+r`
- Windows: `ctrl+shift+r`
- OSX:     `ctrl+meta+r`

### Using Command Palette:

As defined in `Default.sublime-commands` file:

	[
	    { "caption": "User: Python PEP8 Autoformat", "command": "pep8_autoformat" }
	]

You can reformat code by opening Command Palette (ctrl+shift+P) and type "auto"...
to highlight full caption.

## License

Copyright 2012 Stéphane Bunel

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
