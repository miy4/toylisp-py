from __future__ import annotations

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
"""A Scheme environment is a mapping of {variable: value}."""
Env = dict

LPAREN = "("
RPAREN = ")"
DEFINE = "define"


def standard_env() -> Env:
    """Return an environment with some Scheme standard procedures."""
    return Env()


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
    if isinstance(expr, Number):
        return expr
    if expr[0] == DEFINE:
        (_, symbol, args) = expr
        env[symbol] = evaluate(args, env)
        return None

    msg = f"Unknown expression: {expr}"
    raise ValueError(msg)
