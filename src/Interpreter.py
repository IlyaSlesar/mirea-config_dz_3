import argparse
import toml

# Обработка арифметических операций
def evaluate_expression(expression, constants):
    stack = []
    tokens = expression.split()
    print(tokens)
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in constants:
            stack.append(constants[token])
        elif token in ['+', '-', '*', '/', 'concat()', 'sort()']:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
            elif token == 'concat()':
                stack.append(str(a) + str(b))
            elif token == 'sort()':
                stack.append('list(' + str(sorted([a, b])) + ')')
        else:
            raise ValueError(f"Unknown token in expression: {token}")
    return stack[0]

# Трансформация данных
def transform_to_custom_language(data, constants=None):
    if constants is None:
        constants = {}
    result = []
    for key, value in data.items():
        print(key, value)
        if isinstance(value, dict):  # Рекурсивная обработка
            result.append(f"var {key} = {{")
            result.append(transform_to_custom_language(value, constants))
            result.append("}")
        elif isinstance(value, list):  # Обработка массивов
            items = ', '.join(map(str, value))
            result.append(f"var {key} = list({items})")
        elif str(value).startswith("?"):  # Выражения
            expression = value[2:-1].strip()
            computed_value = evaluate_expression(expression, constants)
            result.append(f"{key} = {computed_value}")
        elif isinstance(value, str):  # Обработка строк
            result.append(f'var {key} = @"{value}"')
        elif isinstance(value, (int, float)):  # Числа
            constants[key] = value
            result.append(f"var {key} = {value}")
        else:
            raise ValueError(f"Unsupported data type for key: {key}")
    return "\n".join(result)

# Основной скрипт
def main():
    parser = argparse.ArgumentParser(description="Convert TOML to custom configuration language.")
    parser.add_argument("--input", "-i", required=True, help="Path to input TOML file")
    parser.add_argument("--output", "-o", required=True, help="Path to output configuration file")
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as toml_file:
            data = toml.load(toml_file)
    except Exception as e:
        print(f"Error reading TOML file: {e}")
        return

    try:
        result = transform_to_custom_language(data)
        with open(args.output, 'w') as output_file:
            output_file.write(result)
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
