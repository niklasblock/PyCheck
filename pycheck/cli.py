#pycheck/cli.py

import argparse
import sys 
from pathlib import Path

from .analyzer import Analyzer

def main() -> None:
    """Entry point for the pycheck CLI."""
    path = get_cli_argument() 

    analyzer = Analyzer(path) 
    warnings = analyzer.analyze()

    print_report(path, warnings)


def get_cli_argument() -> Path: 
    """Parse and validate the CLI file argument.
    
    Returns:
        Path: validated .py file path
    
    Exits:
        1: if file does not exist or is not a .py file
    """
    parser = argparse.ArgumentParser(description="Analysiert Python-Dateien")
    parser.add_argument("file", help="Die zu analysierende Python-Datei")
    args = parser.parse_args() # Argument einlesen
    path = Path(args.file) # Zugriff auf den Wert und diesen zu einenm Pfad machen 
    if not path.exists(): 
        print("Kein gültiger Pfad", file=sys.stderr)
        sys.exit(1)

    if path.suffix != ".py": 
        print("Der Pfad ist keinen .py Datei!", file=sys.stderr)
        sys.exit(1)

    return path 

def print_report(path: Path, warnings: list[str]) -> None: 
    """Print report of all warnings"""
    print(f"Analysiere: {path}\n") # Fürs logging in der Console
    if warnings: 
        print(f"⚠ {len(warnings)} Problem(e) gefunden: ")
        for warning in warnings: 
            print(f"  {warning}") 
    else: 
        print("✓ Keine Probleme gefunden.")

if __name__ == "__main__": 
    main()