from .lisp import (
    evaluate,
    parse,
    tokenize,
)


def test_tokenize():
    expected = ["(", "*", "pi", "(", "*", "r", "r", ")", ")"]
    assert expected == tokenize("(* pi (* r r))")


def test_parse():
    expected = ["begin", ["define", "r", 10], ["*", "pi", ["*", "r", "r"]]]
    assert expected == parse("(begin (define r 10) (* pi (* r r)))")


def test_evaluate_atom():
    expected = 1
    assert expected == evaluate(parse("1"))
