"""Copyright 2021 deverte. All rights reserved.
Use of this source code is governed by a BSD-like license that can be found in
the LICENSE file.

Contents:
`Shortcuts` class for loading and parsing JSON file, and creating shortcuts.

Typical usage example:

    import shortcuts

    sc = shortcuts.Shortcuts()
    sc.load("shortcuts.json")
    sc.link()
"""

import json
import os
import sys

import winshell

class Shortcuts:
    """Container for shortcuts loading, parsing and creating."""
    def __init__(self):
        self._path: str = None
        self._json: object = None
        self._parsed: list = []

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value

    @property
    def json(self) -> object:
        return self._json

    @json.setter
    def json(self, value: object):
        self._json = value

    @property
    def parsed(self) -> list:
        return self._parsed

    @parsed.setter
    def parsed(self, value: list):
        self._parsed = value

    def _parse(self):
        """Parses JSON file with variables substitution."""
        match self.json:
            case {"variables": dict(variables), "shortcuts": list(shortcuts)}:
                for shortcut in shortcuts:
                    parsed_shortcut = shortcut
                    parsed_shortcut["name"] = substitute_variables(parsed_shortcut["name"], variables)
                    parsed_shortcut["src"] = substitute_variables(parsed_shortcut["src"], variables)
                    if "args" in parsed_shortcut.keys():
                        parsed_shortcut["args"] = substitute_variables(parsed_shortcut["args"], variables)
                    else:
                        parsed_shortcut["args"] = ""
                    if "icon" in parsed_shortcut.keys():
                        icon = parsed_shortcut["icon"][0]
                        idx = int(parsed_shortcut["icon"][1])
                        parsed_shortcut["icon"][0] = substitute_variables(icon, variables)
                    else:
                        parsed_shortcut["icon"] = ["", 0]
                    parsed_shortcut["dst"] = substitute_variables(parsed_shortcut["dst"], variables)
                    self.parsed.append(parsed_shortcut)


    def load(self, path: str):
        """Loads and parses JSON file with shortcuts description."""
        self.path = path

        try:
            with open(self.path, 'r', encoding="utf-8") as read_file:
                self.json = json.load(read_file)
        except:
            print(f"File reading error: {self.path}")
            sys.exit()
            
        self._parse()

    def link(self):
        """Creates shortcuts."""
        for shortcut in self.parsed:
            os.makedirs(shortcut["dst"], exist_ok=True)
            try:
                winshell.CreateShortcut(
                    Path=os.path.join(shortcut["dst"], f'{shortcut["name"]}.lnk'),
                    Target=shortcut["src"],
                    Arguments=shortcut["args"],
                    Icon=shortcut["icon"])
            except:
                dst = os.path.join(shortcut["dst"], f'{shortcut["name"]}')
                print(f'Error: src="{shortcut["path"]}", dst="{dst}.lnk"')

def substitute_variables(string: str, mapping: dict) -> str:
    """Substitutes variables from mapping into string.
    
    Variables in string must be in `${var}` format.

    Example:
    >>> hello = "${language}: ${translation}!"
    >>> mapping_en = {"language": "English", "translation": "Hello, World!"}
    >>> mapping_en = {"language": "Russian", "translation": "Здравствуй, Мир!"}
    >>> 
    >>> substitute_variables(hello, mapping_en) # English: Hello, World!
    >>> substitute_variables(hello, mapping_ru) # Russian: Здравствуй, Мир!
    """
    for variable, target in mapping.items():
        string = string.replace(f"${{{variable}}}", target)
    return string
