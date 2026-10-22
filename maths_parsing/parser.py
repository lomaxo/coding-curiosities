VALID_OPERATORS = "+-*/()^"
precedence =   {'+': 2, 
                '-': 2, 
                '*': 3, 
                '/': 3,
                '^': 4}

associativity ={'+': 'L', 
                '-': 'L', 
                '*': 'L', 
                '/': 'L',
                '^': 'R'}                

def tokenizer(input_str: str) -> list[str]:
    token_list = []
    next_token = ''
    for char in input_str:
        if char in "1234567890":
            # This could be a multi-digit number
            next_token += char
        elif char in VALID_OPERATORS:
            if next_token:
                token_list.append(next_token)
            token_list.append(char)
            next_token = ''
        elif char == ' ':
            # Ignore spaces, except that they mark the end of a number
            if next_token:
                token_list.append(next_token)
                next_token = ''
        else:
            # Not a valid operator or digit. Something is wrong.
            print(f"Unexpected item in the bagging area: '{char}'")
            return []
    
    # There might be digits still not pushed to the list
    if next_token != '':
        token_list.append(next_token)
    return token_list

def shunting(tokens: list[str]) -> list[str]:
    operators = []
    output_stack = []
    while tokens:
        next_token = tokens.pop(0)
        if next_token.isnumeric():
            output_stack.append(next_token)
        elif next_token == '(':
            operators.append(next_token)
        elif next_token == ')':
            while operators and operators[-1] != '(':
                output_stack.append(operators.pop())
            operators.pop()
        elif next_token in VALID_OPERATORS:
            # If precendence is <= than the current top operator transfer that over to the ouput stack
            while (operators
                    and operators[-1] != '(' 
                    and (precedence[operators[-1]] > precedence[next_token] 
                    or (associativity[next_token] == 'L' and precedence[operators[-1]] == precedence[next_token]))
                    ):
                output_stack.append(operators.pop())
                
            operators.append(next_token)
        else:
            print(f"Unexpected token: '{char}'")
    while operators:
        output_stack.append(operators.pop())
    return output_stack

def evaluate_rpn(rpn: list[str]) -> float:
    stack = []
    while rpn:
        next_token = rpn.pop(0)
        if next_token.isnumeric():
            stack.append(float(next_token))
        elif next_token in VALID_OPERATORS:
            match next_token:
                case '+':
                    op1 = stack.pop()
                    op2 = stack.pop()
                    stack.append(op1+op2)
                case '-':
                    op2 = stack.pop()
                    op1 = stack.pop()
                    stack.append(op1-op2)
                case '*':
                    op1 = stack.pop()
                    op2 = stack.pop()
                    stack.append(op1*op2)
                case '/':
                    op2 = stack.pop()
                    op1 = stack.pop()
                    stack.append(op1/op2)
                case '^':
                    op2 = stack.pop()
                    op1 = stack.pop()
                    stack.append(op1**op2)
                case _:
                    print(f"Unhandled operator in rpn: '{next_token}'")
                    return
        else:
            print("Unknown token in rpn")
    if len(stack) != 1:
        print('Incomplete expression?')
        return stack
    return stack[0]

# expression = "2^3^2"
expression = "5-2-1"

print(f"expr: '{expression}'")
tokens = tokenizer(expression)
print(f'tokens: {tokens}')
rpn = shunting(tokens)
print(f'rpn: {rpn}')
result = evaluate_rpn(rpn)
print(f'result: {result}')
