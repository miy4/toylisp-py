from __future__ import annotations

import math
import operator as op

"""A Scheme Symbol is implemented as a Python str."""
Symbol = str
"""A Scheme Number is implemented as a Python int or float."""
Number = (int, float)
"""A Scheme Atom is a Symbol or Number."""
Atom = (Symbol, Number)
"""A Scheme List is implemented as a Python list"""
List = list
"""A Scheme expression is an Atom or List."""
Exp = (Atom, List)

LPAREN = "("
RPAREN = ")"
DEFINE = "define"
IF_COND = "if"
QUOTE = "quote"
SET_BANG = "set!"


class Env(dict):
    """A Scheme environment is a mapping of {variable: value}."""

    def __init__(
        self,
        parms: tuple[str] = (),
        args: tuple[Exp] = (),
        outer: Env | None = None,
    ) -> None:
        """Initialize the Env object."""
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var: str) -> Env:
        """Find the innermost Env where var appears."""
        return self if var in self else self.outer.find(var)


def standard_env() -> Env:
    """Return an environment with some Scheme standard procedures."""
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "apply": lambda proc, args: proc(*args),
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x, *y],
            "eq?": op.is_,
            "expt": pow,
            "equal?": op.eq,
            "length": len,
            "list": lambda *x: List(x),
            "list?": lambda x: isinstance(x, List),
            "map": map,
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, Number),
            "print": print,
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
        },
    )
    return env


global_env = standard_env()


def tokenize(chars: str) -> list[str]:
    """Convert a string of characters into a list of tokens."""
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def read_from_tokens(tokens: list[str]) -> Exp:
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        msg = "unexpected EOF"
        raise SyntaxError(msg)

    token = tokens.pop(0)
    if token == LPAREN:
        l = []
        while tokens[0] != RPAREN:
            l.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return l

    if token == RPAREN:
        msg = f"unexpected {RPAREN}"
        raise SyntaxError(msg)

    return atom(token)


def atom(token: str) -> Atom:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def parse(program: str) -> Exp:
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenize(program))


def evaluate(expr: Exp, env: Env = global_env) -> Exp | None:
    """Evaluate an expression in an environment."""
    if isinstance(expr, Symbol):  # variable reference
        return env.find(expr)[expr]
    if isinstance(expr, Number):  # constant
        return expr

    op, *args = expr
    if op == QUOTE:  # quotation
        return args[0]
    if op == IF_COND:  # conditional
        (test, conseq, alt) = args
        exp = conseq if evaluate(test, env) else alt
        return evaluate(exp, env)
    if op == DEFINE:  # definition
        (symbol, exp) = args
        env[symbol] = evaluate(exp, env)
        return None
    if op == SET_BANG:
        symbol, exp = args
        env.find(symbol)[symbol] = evaluate(exp, env)
        return None

    proc = evaluate(op, env)  # procedure call
    vals = [evaluate(arg, env) for arg in args]
    return proc(*vals)


def schemestr(expr: Exp) -> str:
    """Convert a Python object back into a Scheme-readable string."""
    if isinstance(expr, List):
        return "(" + " ".join(map(schemestr, expr)) + ")"
    return str(expr)


def repl(prompt: str = "lis.py> "):
    """Execute a prompt-read-eval-print loop."""
    while True:
        val = evaluate(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))
