import argparse
import toml

# Обработка арифметических операций
def evaluate_expression(expression, constants):
    stack = []
    tokens = expression.split()
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
                stack.append('list(' + ', '.join(map(str, sorted([a, b]))) + ')')
        else:
            raise ValueError(f"Unknown token in expression: {token}")
    return stack[0]

def transform_list(list_in, constants = None):
    for i in range(len(list_in)):
        if isinstance(list_in[i], dict):  # Рекурсивная обработка
            list_in[i] = '{\n' + transform_to_custom_language(list_in[i], constants) + '\n}'
        if isinstance(list_in[i], list):
            list_in[i] = transform_list(list_in[i])
        elif str(list_in[i]).startswith('?['):
            expression = str(list_in[i][2:-1]).strip()
            computed_value = evaluate_expression(expression, constants)
            list_in[i] = computed_value
        elif isinstance(list_in[i], str):
            list_in[i] = f'@"{list_in[i]}"'
        elif isinstance(list_in[i], (int, float)):
            list_in[i] = str(list_in[i])
        else:
            raise ValueError(f"Unsupported data type for list item: {list_in[i]}")
    return "list(" + ', '.join(list_in) + ")"

# Трансформация данных
def transform_to_custom_language(data, constants=None):
    if constants is None:
        constants = {}
    result = []
    for key, value in data.items():
        if isinstance(value, dict):  # Рекурсивная обработка
            result.append(f"var {key} = {{")
            result.append(transform_to_custom_language(value, constants))
            result.append("}")
        elif isinstance(value, list):  # Обработка массивов
            result.append(f"var {key} = {transform_list(value, constants)}")
        elif str(value).startswith("?["):  # Выражения
            expression = value[2:-1].strip()
            computed_value = evaluate_expression(expression, constants)
            result.append(f"var {key} = {computed_value}")
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
