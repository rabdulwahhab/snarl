# Alon
SwDev Spring 2021 project repository for rayyan3 and sfarooqui18

----------------

## Snarl

### Distribution

Clone and install dependencies in the `Snarl/` 

  pip install -r requirements.txt

Use `./bin/pip3.6` for pkg management

Remember to activate the Venv with `source bin/activate` for all proj related commands

## To run tests:

    pytest

## To build an executable, nav to the program dir and

    pyinstaller [program].py

### Debug Notes:
- If `ModuleNotFound`, try checking `PYTHONPATH` and adding proj dir to it

    export PYTHONPATH=$PYTHONPATH:.

