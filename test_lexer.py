import pytest
from lexer import analyze_code  

def test_keywords():
    code = "int x = 10;"
    result = analyze_code(code)
    assert "Keywords: ['int']" in result

def test_identifier():
    code = "variable_name = 5;"
    result = analyze_code(code)
    assert "Identifiers: ['variable_name']" in result

def test_operator():
    code = "a + b;"
    result = analyze_code(code)
    assert "Operators: ['+']" in result

def test_constant():
    code = "x = 42;"
    result = analyze_code(code)
    assert "Constants: ['42']" in result

def test_punctuation():
    code = "func();"
    result = analyze_code(code)
    assert "Punctuation: ['(', ')', ';']" in result

def test_literal():
    code = 'string = "hello";'
    result = analyze_code(code)
    assert 'Literals: [\'"hello"\']' in result
