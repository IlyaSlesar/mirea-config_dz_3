import pytest
from Interpreter import transform_to_custom_language, evaluate_expression

# Тест обработки чисел
def test_numbers():
    input_data = {"number": 42}
    expected_output = "var number = 42"
    assert transform_to_custom_language(input_data) == expected_output

# Тест обработки строк
def test_strings():
    input_data = {"greeting": "Hello, world!"}
    expected_output = 'var greeting = @"Hello, world!"'
    assert transform_to_custom_language(input_data) == expected_output

# Тест обработки массивов
def test_arrays():
    input_data = {"list_example": ["item1", "item2", "item3"]}
    expected_output = 'var list_example = list(@"item1", @"item2", @"item3")'
    assert transform_to_custom_language(input_data) == expected_output

# Тест вложенных структур
def test_nested_structures():
    input_data = {
        "outer": {
            "inner": {
                "key": 10,
                "value": "test"
            }
        }
    }
    expected_output = (
        "var outer = {\n"
        "var inner = {\n"
        "var key = 10\n"
        "var value = @\"test\"\n"
        "}\n"
        "}"
    )
    assert transform_to_custom_language(input_data) == expected_output

# Тест вычислений выражений
def test_expressions():
    constants = {"a": 5, "b": 3}
    expression = "a b +"
    result = evaluate_expression(expression, constants)
    assert result == 8

# Тест трансформации выражений
def test_expression_transformation():
    input_data = {"result": "?[a b +]"}
    constants = {"a": 2, "b": 3}
    expected_output = "var result = 5"
    assert transform_to_custom_language(input_data, constants) == expected_output

# Тест ошибок в выражениях
def test_invalid_expression():
    constants = {"a": 5, "b": 3}
    invalid_expression = "a b unknown_op"
    with pytest.raises(ValueError, match="Unknown token in expression: unknown_op"):
        evaluate_expression(invalid_expression, constants)

# Тест обработки многомерных массивов
def test_multidimensional_arrays():
    input_data = {"matrix": [[1, 2], [3, 4]]}
    expected_output = "var matrix = list(list(1, 2), list(3, 4))"
    assert transform_to_custom_language(input_data) == expected_output

# Тест сложной конфигурации
def test_complex_configuration():
    input_data = {
        "config": {
            "name": "Test",
            "settings": {
                "option1": 1,
                "option2": ["a", "b", "c"],
                "option3": {
                    "nested": "value"
                }
            }
        }
    }
    expected_output = (
        "var config = {\n"
        "var name = @\"Test\"\n"
        "var settings = {\n"
        "var option1 = 1\n"
        "var option2 = list(@\"a\", @\"b\", @\"c\")\n"
        "var option3 = {\n"
        "var nested = @\"value\"\n"
        "}\n"
        "}\n"
        "}"
    )
    assert transform_to_custom_language(input_data) == expected_output
