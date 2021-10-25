"""Copyright 2021 deverte. All rights reserved.
Use of this source code is governed by a BSD-like license that can be found in
the LICENSE file.

Contents:
Program that creates shortcuts (soft links) according to the template described
in the JSON file. You can define your variables (paths, executables, parameters
and etc.) in `variables` section and use them in shortcuts definition.
Target operating system: Windows.

JSON file format:

```json
{
    "variables": {
        "<variable>": "<value>",
        ...
    },
    "shortcuts": [
        {
            "name": "<shortcut name>",
            "src": "<path to reference file>",
            "args": "<arguments to a reference file>",
            "dst": "<path to a shortcut>",
            "icon": ["<path to an icon/executable/dll>", <N>]
        },
        ...
    ]
}
```

> Note: `args` and `icon` fields are optional.



Typical usage example:
"""

import argparse

import shortcuts

def main():
    parser = argparse.ArgumentParser(
        description="Creates shortcuts according to the template described in"
                    "the JSON file.")
    parser.add_argument("shortcuts", type=str, help="JSON file with shortcuts.")

    args = parser.parse_args()

    sc = shortcuts.Shortcuts()
    sc.load(args.shortcuts)
    sc.link()

if __name__ == "__main__":
    main()