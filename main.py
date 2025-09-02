import re

def parse_expression():
    while True:
        try:
            expression = input("Введите выражение: ")
            clean_expr = expression.replace(" ", "")
            match = re.match(r'(\d+)([\+\-\*\:\/])(\d+)', clean_expr)

            if not match:
                raise ValueError("Неверный формат выражения")

            arg1, operator, arg2 = match.groups()

            if operator not in "+-*/:":
                raise ValueError

            if '.' in arg1 or '.' in arg2:
                print("Ошибка: обнаружены дробные числа. Пожалуйста, используйте только целые числа.")
                continue

            return arg1, operator, arg2

        except ValueError:
            print("Не корректное выражение! Попробуйте снова.")

def print_expression(expression_string):
    arg1 = int(expression_string[0])
    arg2 = int(expression_string[2])
    operator = expression_string[1]
    len_greater_arg = len(str(max(abs(arg1), abs(arg2)))) + 2
    match operator:
        case "+":
            res = arg1 + arg2
            result_string = f'{'+':<{len_greater_arg - len(str(abs(arg1)))}}{arg1}\n  {arg2}\n{'-' * len_greater_arg}\n{res}'
            return '\n'.join(f'{line:>50}' for line in result_string.splitlines())
        case "-":
            res = arg1 - arg2
            result_string = f'{'-':<{len_greater_arg - len(str(abs(arg1)))}}{arg1}\n  {arg2}\n{'-' * len_greater_arg}\n{res}'
            return '\n'.join(f'{line:>50}' for line in result_string.splitlines())
        case "*":
            res = arg1 * arg2
            digits_numbers = list(str(arg2))[::-1]
            result_string = f'{'*':<{len_greater_arg - len(str(abs(arg1)))}}{arg1}\n  {arg2}\n{'-' * len_greater_arg}\n'
            result_string += ''.join(f'{arg1 * int(digit)}\n' for digit in digits_numbers)
            shift_digits = '\n'.join(f'{line:>{50 - ((i - 4) if i >= 4 else 0)}}' for i,line in enumerate(result_string.splitlines(), start=1))
            return shift_digits + f'\n{('-' * len_greater_arg):>50}\n{res:>50}'
        case "/" | ":":
            if arg2 == 0:
                raise ValueError('Деление на ноль!')

            arg1_str = str(arg1)
            quotient_str = ""
            remainder = 0
            steps = []
            started = False
            i = 0

            while i < len(arg1_str):
                current = remainder * 10 + int(arg1_str[i])
                if current < arg2 and not started:
                    quotient_str += "0"
                    remainder = current
                    i += 1
                    continue
                q = current // arg2
                r = current % arg2
                if q != 0 or started:
                    quotient_str += str(q)
                    started = True
                steps.append((i - len(str(current)) + 1, current, q * arg2, r))
                remainder = r
                i += 1

            space_offset = " " * 50

            print(f"{space_offset}{arg1} | {arg2}")

            first_pos, first_current, first_sub, _ = steps[0]
            print(f"{space_offset}{' ' * first_pos}{first_sub}{"":<{len(arg1_str) + 1 - len(str(first_sub))}}| {quotient_str.lstrip('0')}")

            for idx, (pos, current, sub, r) in enumerate(steps):
                if idx == 0:
                    continue

                spaces = pos + len(str(current)) - len(str(sub))
                print(f"{space_offset}{' ' * spaces}{sub}")

                if r != 0:
                    r_str = str(r)
                    r_spaces = pos + len(str(current)) - len(r_str)
                    print(f"{space_offset}{' ' * r_spaces}{r}")

            last_r = steps[-1][3]
            print(f"{space_offset}{str(last_r).rjust(len(str(arg1)))}")
    return None


if __name__ == '__main__':
    parsed_expression = parse_expression()
    print(print_expression(parsed_expression))



