#tests/test_analyzer.py 

import ast 
from pycheck.analyzer import Analyzer
from pathlib import Path 
import pytest
import textwrap
import tempfile
import os 

# --- Missing Docstrings 
def test_missing_docstring(): 
    """one function with Docstring
        -> one warning
    """

    source = textwrap.dedent("""
    def foo(): 
        pass 
    """)

    tree = ast.parse(source) 
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_missing_docstrings(tree) 

    assert len(warnings) == 1 
    assert "foo" in warnings[0]

def test_no_missing_docstring(): 
    """one function with Docstring 
        -> no warning, empty list 
    """

    source = textwrap.dedent('''
    def bar():
        """Diese hat einen Docstring."""
        pass
    ''')

    tree = ast.parse(source)
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_missing_docstrings(tree)

    assert len(warnings) == 0 
    assert warnings == []

def test_multiple_missing(): 
    """three functions, two without Docstring
        -> two warnings 
    """

    source = textwrap.dedent('''
    def foo():
        pass

    def bar():
        """Diese hat einen Docstring."""
        pass

    def baz():
        pass
    ''')

    tree = ast.parse(source)
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_missing_docstrings(tree) 

    assert len(warnings) == 2
    assert "foo" in warnings[0]
    assert "baz" in warnings[1]


# --- Too many Params 
def test_too_many_params(): 
    """function with five parameters 
        -> one warning 
    """
    
    source = textwrap.dedent("""
    def foo(a, b, c, d, e):
        pass
    """)
    
    tree = ast.parse(source) 
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_too_many_params(tree) 

    assert len(warnings) == 1 
    assert "foo" in warnings[0]

def test_permitted_params(): 
    """function with three parameters
        -> no warning
    """
    
    source = textwrap.dedent("""
    def foo(a, b, c):
        pass
    """)
    
    tree = ast.parse(source) 
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_too_many_params(tree) 

    assert len(warnings) == 0 
    assert warnings == []

# --- Too long function
def test_too_long_function(): 
    """function with  25 lines
        -> one warning 
    """

    body = "\n".join(["    x = 1"] * 25)
    source = f"def foo():\n{body}"

    tree = ast.parse(source)
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_function_too_long(tree)

    assert len(warnings) == 1 
    assert "foo" in warnings[0]

def test_permitted_long_function():
    """function with 10 lines
        -> no warning
    """

    body = "\n".join(["    x = 1"] * 10)
    source = f"def foo():\n{body}"

    tree = ast.parse(source)
    analyzer = Analyzer(Path("dummy.py"))

    warnings = analyzer._check_function_too_long(tree)

    assert len(warnings) == 0  
    assert warnings == []

# --- Syntax Error in file
def test_sytax_error(): 
    """Tempfile with SyntaxError
        -> one warning
    """
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("def foo(:\n    pass\n")
        tmp_path = Path(f.name)
    
    try:
        analyzer = Analyzer(tmp_path)
        warnings = analyzer.analyze()
    finally:
        tmp_path.unlink(missing_ok=True)

    assert len(warnings) == 1
    assert "SyntaxError" in warnings[0]