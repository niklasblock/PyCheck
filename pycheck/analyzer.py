#pycheck/analyzer.py 

import ast 
from pathlib import Path

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
        tree = ast.parse(source)

        missing_docstrings = self._check_missing_docstrings(tree)
        too_many_params = self._check_too_many_params(tree)

        return missing_docstrings + too_many_params
          

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
                if len(params) > 4: 
                    too_many_params.append(
                        f"Zeile {node.lineno}: Funktion '{node.name}' hat {len(params)} Parameter"
                    )

        return too_many_params 
