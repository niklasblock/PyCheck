#pycheck/cli.py

import argparse
import sys 
from pathlib import Path

from .analyzer import Analyzer

def main() -> None:
    """Entry point for the pycheck CLI."""
    paths = get_cli_argument() 
    
    for path in paths: 
        analyzer = Analyzer(path) 
        warnings = analyzer.analyze()

        print_report(path, warnings)


def get_cli_argument() -> list[Path]: 
    """Parse and validate the CLI file argument.
    
    Returns:
        Paths: validated List of .py file paths
    
    Exits:
        1: if file does not exist or is not a .py file
    """
    parser = argparse.ArgumentParser(description="Analysiert Python-Dateien")
    parser.add_argument("files", nargs="+", help="Die zu analysierende Python-Datei")
    args = parser.parse_args() # Argumente einlesen
    
    paths = []
    for file in args.files: 
        path = Path(file)
        if not path.exists():
            print(f"Kein gültiger Pfad: {path}", file=sys.stderr)
            sys.exit(1) 

        if path.suffix != ".py": 
            print(f"Der Pfad ist keine .py Datei: {path}", file=sys.stderr)
            sys.exit(1)
        
        paths.append(path)

    if len(paths) == 0: 
        print("Es wurde kein gültiges Programm gefunden! Programm beendet!", file=sys.stderr)
        sys.exit(1)

    return paths 
 

def print_report(path: Path, warnings: list[str]) -> None: 
    """Print report of all warnings"""
    print(f"Analysiere: {path}\n") # Fürs logging in der Console
    if warnings: 
        print(f"⚠ {len(warnings)} Problem(e) gefunden: ")
        for warning in warnings: 
            print(f"  {warning}") 
    else: 
        print("✓ Keine Probleme gefunden.")
    
    print("-" * 40)

if __name__ == "__main__": 
    main()