"""제한된 다항식 문법을 정확한 유리수 계수로 계산합니다."""
import ast
from fractions import Fraction


def polynomial(text):
    text = text.strip().replace('^', '**')
    if not text or len(text) > 150:
        raise ValueError('수식을 150자 이내로 입력해 주세요.')
    try:
        tree = ast.parse(text, mode='eval')
    except SyntaxError as exc:
        raise ValueError('곱셈은 *로, 거듭제곱은 ^로 입력해 주세요.') from exc
    if len(list(ast.walk(tree))) > 100:
        raise ValueError('수식을 더 짧게 입력해 주세요.')

    def clean(p):
        if any(degree > 12 or abs(coefficient) > 10**15 for degree, coefficient in p.items()):
            raise ValueError('12차 이하의 작은 계수 다항식을 입력해 주세요.')
        return {degree: coefficient for degree, coefficient in p.items() if coefficient}

    def add(a, b):
        out = a.copy()
        for degree, value in b.items():
            out[degree] = out.get(degree, Fraction(0)) + value
        return clean(out)

    def multiply(a, b):
        out = {}
        for i, av in a.items():
            for j, bv in b.items():
                out[i+j] = out.get(i+j, Fraction(0)) + av*bv
        return clean(out)

    def read(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 10**6:
                raise ValueError('숫자의 크기는 100만 이하로 입력해 주세요.')
            return clean({0: Fraction(str(node.value))})
        if isinstance(node, ast.Name) and node.id == 'x':
            return {1: Fraction(1)}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            p = read(node.operand)
            return {k: (-v if isinstance(node.op, ast.USub) else v) for k, v in p.items()}
        if isinstance(node, ast.BinOp):
            a, b = read(node.left), read(node.right)
            if isinstance(node.op, ast.Add):
                return add(a, b)
            if isinstance(node.op, ast.Sub):
                return add(a, {k: -v for k, v in b.items()})
            if isinstance(node.op, ast.Mult):
                return multiply(a, b)
            if isinstance(node.op, ast.Div) and set(b) == {0}:
                return clean({k: v / b[0] for k, v in a.items()})
            if isinstance(node.op, ast.Pow) and set(b).issubset({0}):
                exponent = b.get(0, Fraction(0))
                if exponent.denominator == 1 and 0 <= exponent <= 6:
                    out = {0: Fraction(1)}
                    for _ in range(int(exponent)):
                        out = multiply(out, a)
                    return out
        raise ValueError('x, 숫자, 괄호와 + - * / ^만 사용할 수 있습니다. 나눗셈의 분모는 0이 아닌 상수여야 합니다.')

    return read(tree.body)
