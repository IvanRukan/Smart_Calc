import re
from collections import deque


def variable_assignment(inp):
    inp = ''.join(inp)
    template = '[a-zA-z]+='
    if re.match(template, inp):
        if re.match('([a-zA-z]+)=([A-za-z\d]+)$', inp):
            var = re.match('([a-zA-z]+)=([A-za-z\d]+)', inp).groups()
            return var
        else:
            print('Invalid assignment')
    else:
        print('Invalid identifier')


def true_operations(expr):
    if re.search('(\*\*)+', expr):
        return None
    if re.search('(//)+', expr):
        return None
    expr = re.sub('\++', '+', expr)
    expr = re.sub('(--)+', '+', expr)
    expr = re.sub('\+-', '-', expr)
    return expr


def from_infix_to_postfix(expr):
    new = []

    for each in expr:
        if '(' in each:
            for _ in range(each.count('(')):
                new.append('(')
            new.append(each.strip('('))
            continue
        elif ')' in each:
            new.append(each.strip(')'))
            for _ in range(each.count(')')):
                new.append(')')
            continue
        new.append(each)
    expr = new
    left = expr.count('(')
    right = expr.count(')')
    if left != right:
        return None
    res = []
    ops = deque()
    for element in expr:
        if element.isdigit() or element.isalpha():
            res.append(element)
        else:
            if not ops or ops[-1] == '(':
                ops.append(element)
            elif element in '*/' and ops[-1] in '+-':
                ops.append(element)
            elif element in '-+' and ops[-1] in '*/' or element in '+-' and ops[-1] in '+-' or element in '*/' and ops[
                -1] in '/*':
                while ops[-1] != '(':
                    if ops[-1] in '+-' and element in '*/':
                        break
                    next_op = ops.pop()
                    res.append(next_op)
                    if not ops:
                        break
                ops.append(element)
            elif element == '(':
                ops.append(element)
            elif element == ')':
                while ops[-1] != '(':
                    next_op = ops.pop()
                    res.append(next_op)
                ops.pop()
    else:
        ops = ''.join(ops)
        for each in ops[::-1]:
            res.append(each)
    return res


def from_postfix_to_answer(expr):
    answer = deque()
    for each in expr:
        if each.isdigit() or each.lstrip('-').isdigit():
            answer.append(each)
        elif each == '+':
            b = answer.pop()
            a = answer.pop()
            answer.append(addition(a, b))
        elif each == '*':
            b = answer.pop()
            a = answer.pop()
            answer.append(multiplication(a, b))
        elif each == '-':
            b = answer.pop()
            a = answer.pop()
            answer.append(subtraction(a, b))
        elif each == '/':
            b = answer.pop()
            a = answer.pop()
            answer.append(division(a, b))
    return answer[0]


def addition(a, b):
    return int(a) + int(b)


def subtraction(a, b):
    return int(a) - int(b)


def multiplication(a, b):
    return int(a) * int(b)


def division(a, b):
    return int(a) / int(b)


def calculator():
    variables = {}
    while True:
        user_input = input().split()
        if len(user_input) == 1:
            if user_input[0] == '/exit':
                print('Bye!')
                break
            elif user_input[0] == '/help':
                print('The program calculates can add, subtract, multiply or divide numbers or given variables. ')
            elif user_input[0].isdigit() or user_input[0].lstrip('-').isdigit() or user_input[0].lstrip('+').isdigit():
                print(user_input[0].lstrip('+'))
            elif '/' in user_input[0]:
                print('Unknown command')
            else:
                if re.match('[a-zA-z]+=?', user_input[0]):
                    if user_input[0] in variables:
                        print(variables[user_input[0]])
                    elif re.match('[a-zA-z]+=[a-zA-z\d]+', user_input[0]):
                        new_var = variable_assignment(user_input)
                        if new_var:
                            if new_var[1] in variables:
                                variables[new_var[0]] = variables[new_var[1]]
                            else:
                                if new_var[1].isdigit():
                                    variables[new_var[0]] = new_var[1]
                                else:
                                    print('Invalid assignment')
                            continue
                        else:
                            continue
                    else:
                        print('Unknown variable')
                else:
                    print('Invalid identifier')
        else:
            if not user_input:
                continue
            user_input = [element.strip() for element in user_input]
            if '=' in user_input:
                new_var = variable_assignment(user_input)
                if new_var:
                    if new_var[1] in variables:
                        variables[new_var[0]] = variables[new_var[1]]
                        continue
                    else:
                        if new_var[1].isdigit():
                            variables[new_var[0]] = new_var[1]

                        else:
                            print('Invalid assignment')
                        continue
                else:
                    continue
            user_input = ' '.join(user_input)
            user_input = true_operations(user_input)
            if not user_input:
                print('Invalid expression')
                continue
            user_input = user_input.split()
            for index, element in enumerate(user_input):
                if element in variables:
                    user_input[index] = variables[element]
            user_input = from_infix_to_postfix(user_input)
            if not user_input:
                print('Invalid expression')
                continue
            print(from_postfix_to_answer(user_input))


calculator()
