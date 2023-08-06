# CreateKiCADProject Script

This repository contains a script for use with my KiCAD Template and KiCAD Libraries.

The script asks the user to enter some information for the cookiecutter template.

It then initiates and commits the project to the repository URL provided and installs the library submodule.

## Requirements

### tkinter

#### brew
```sh
brew install python-tk
```

#### apt
```sh
sudo apt-get install python3-tk 
```

#### Windows

see [installation prompt](https://i.stack.imgur.com/yivqM.png)

## Usage

```sh
python CreateKiCADProject.py
```

This should fetch the cookiecutter packages and open the GUI to run the template.

