# pycheck

CLI-Tool das Python-Dateien auf Clean-Code analysiert

## Installation

```bash
git clone https://github.com/niklasblock/PyCheck.git
cd pycheck
pip install -e .
```

## Usage

```bash
pycheck myfile.py
pycheck src/*.py
```

## Checks 
- Functions without docstrings
- Functions with more than 4 parameters
- Functions longer than 20 lines
- Lines longer than 79 characters
- Bare except blocks without eception type

## Development

```bash
pytest tests/
```