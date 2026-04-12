#pycheck/analyzer.py 

import ast 
from pathlib import Path
import sys

class Analyzer: 

    def __init__(self, path: Path) -> None: 
        """Initialize Analyzer with the path to a Python file.
    
        Args:
            path: Path to the .py file to analyze
        """
        self.path = path 

    def analyze(self) -> list[str]:
        """Analyse Path File 
    
        Returns:
            List: Warning str of missing docstrings
        """
        source = self.path.read_text() 
        try: 
            tree = ast.parse(source)
        except SyntaxError as e: 
            return [f"SyntaxError - Zeile {e.lineno}: {e.msg}"]

        missing_docstrings = self._check_missing_docstrings(tree)
        too_many_params = self._check_too_many_params(tree)
        too_long_functions = self._check_function_too_long(tree)
        too_long_lines = self._check_line_too_long(source)

        return missing_docstrings + too_many_params + too_long_functions + too_long_lines
          

    def _check_missing_docstrings(self, tree: ast.AST) -> list[str]: 
        """Check file for missing docstrings 
        
        Returns: 
            List: Warning str of missing docstrings 
        """
        missing_docstrings: list[str] = []
        for node in ast.walk(tree): 
            if isinstance(node, ast.FunctionDef): 
                # print(node.name)
                if not ast.get_docstring(node): 
                    # print("Es wurde kein Docstring gefunden!")
                    missing_docstrings.append(
                        f"Zeile {node.lineno}: Funktion '{node.name}' hat keinen Docstring"
                    )

        return missing_docstrings

    def _check_too_many_params(self, tree: ast.AST) -> list[str]: 
        """Check file for to many params
        
        Returns: 
            List: Warning str of to many params
        """
        too_many_params: list[str] = []
        for node in ast.walk(tree): 
            if isinstance(node, ast.FunctionDef): 
                params = node.args.args # Liste der Parameter 
                filtered_params = [x for x in params if x.arg != "self"] # Liste der Parameter ohne self
                if len(filtered_params) > 4: 
                    too_many_params.append(
                        f"Zeile {node.lineno}: Funktion '{node.name}' hat {len(filtered_params)} Parameter"
                    )

        return too_many_params 

    def _check_function_too_long(self, tree: ast.AST) -> list[str]: 
        """Check file for to long functions
        
        Returns: 
            List: Warning str of to long functions 
        """
        function_too_long: list[str] = []
        for node in ast.walk(tree): 
            if isinstance(node, ast.FunctionDef): 
                length = node.end_lineno - node.lineno 
                if length > 20: 
                    function_too_long.append(
                        f"Zeile {node.lineno}: Funktion '{node.name}' ist zu lang ({length} Zeilen, max. 20)"
                    )
        
        return function_too_long
    
    def _check_line_too_long(self, source: str) -> list[str]: 
        """Check line for too many charaters

        Returns: 
            List: Warning str of too long lines
        """
        lines = source.splitlines() 
        
        lines_too_long: list[str] = []
        for i, line in enumerate(lines):
            if len(line) > 79: 
                lines_too_long.append(
                    f"Zeile {i + 1}: Zeile zu lang ({len(line)} Zeichen, max 79)"
                )

        return lines_too_long