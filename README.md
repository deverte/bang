# Bang

Bang is a program that creates shortcuts (soft links) according to the template
described in the JSON file.

---

- [About](#about)
- [Install](#install)
- [Usage](#usage)
- [Shortcuts File Format](#shortcuts-file-format)
- [License](#license)
- [Build Instructions](#build-instructions)

---

## About

You can define your variables (paths, executables, parameters and etc.) in `variables` section and use them in shortcuts definition. Target operating system: Windows.

Cases when the application may be useful to you:

- If you have a large collection of portable standalone applications or portable applications in many different launchers (e.g. PortableApps, SyMenu, Scoop, ...).
- If you have a cloud-based drive with applications.
- If you want to create a reproducible environment.
- If you want to conveniently create many links to an application with different parameters/options (e.g. with different profiles).

Cases when you don't need the app:

- If you install all applications directly into the system.

## Install

### First method — Scoop

1. Add repo (if not already added).

```sh
scoop bucket add shell https://github.com/deverte/scoop-shell
```

2. Download and install `Bang`.

```sh
scoop install bang
```

Or without adding a repo:

```sh
scoop install https://github.com/deverte/scoop-shell/raw/master/bucket/bang.json
```

### Second method — Direct download

Also you can download a [package](https://github.com/deverte/bang/releases) and unpack it via any ZIP archiver (program is fully portable).

> This method involves manually adding the path to the program to the PATH environment variable.

## Usage

Typical usage:

```sh
bang shortcuts.json
```

Where `shortcuts.json` is a file with shortcuts desctiption.

## Shortcuts File Format

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

In variables section you can define paths, executables, parameters, and etc. to substitute them into shortcuts arguments. For example, `"windir": "C:\\Windows"` will be substituted into `"src": "${windir}\\regedit.exe"`, and result will be `"src": "C:\\Windows\\regedit.exe"`.

## License

This package is distributed under the terms of the [MIT license](./LICENSE).

## Build Instructions

All dependencies can be installed using [Poetry](https://python-poetry.org/).

```sh
poetry install
```

Building:

```sh
poetry run pyinstaller ./bang/main.py --distpath ./dist -F -p ./bang -n bang --exclude-module _bootlocale
```