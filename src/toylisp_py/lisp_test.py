from .lisp import (
    evaluate,
    global_env,
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


def test_evaluate_define_constant():
    expected = 10
    assert evaluate(parse("(define a 10)")) is None
    assert expected == global_env["a"]


def test_evaluate_math_func_call():
    expected = 1.0
    assert expected == evaluate(parse("(cos 0)"))


def test_evaluate_procedure_call():
    expected = 3
    assert expected == evaluate(parse("(+ 1 2)"))

    expected = 314.1592653589793
    assert expected == evaluate(parse("(begin (define r 10) (* pi (* r r)))"))

    expected = [2, 4, 6, 8]
    assert expected == evaluate(
        parse("(list (+ 1 1) (+ 2 2) (* 2 3) (expt 2 3))"),
    )


def test_evaluate_conditional():
    expected = 42
    assert expected == evaluate(parse("(if (> (* 11 11) 120) (* 7 6) oops)"))


def test_evaluate_quote():
    expected = ["the", "more", "the", "bigger", "the", "better"]
    assert expected == evaluate(
        parse("(quote (the more the bigger the better))"),
    )
