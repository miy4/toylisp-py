import pytest

from .lisp import (
    evaluate,
    global_env,
    parse,
    standard_env,
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


def test_evaluate_assignment():
    env = standard_env()
    evaluate(parse("(define a 10)"), env)
    evaluate(parse("(set! a 2)"), env)

    expected = 2
    assert expected == env["a"]


def test_evaluate_procedure():
    env = standard_env()
    evaluate(parse("(define add_one (lambda (n) (+ n 1)))"), env)
    assert evaluate(parse("(add_one 10)"), env) == 11

    evaluate(parse("(define circle-area (lambda (r) (* pi (* r r))))"), env)
    assert evaluate(parse("(circle-area 3)"), env) == pytest.approx(
        28.274333877,
    )

    evaluate(
        parse(
            "(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))",
        ),
        env,
    )
    assert evaluate(parse("(fact 10)"), env) == 3628800
    assert (
        evaluate(parse("(fact 100)"), env)
        == 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
    )
    assert evaluate(parse("(circle-area (fact 10))"), env) == pytest.approx(
        4.1369087198e13,
    )


def test_evaluate_count_words():
    env = standard_env()

    evaluate(parse("(define first car)"), env)
    evaluate(parse("(define rest cdr)"), env)
    expression = "(define count (lambda (item L) (if L (+ (equal? item (first L)) (count item (rest L))) 0)))"
    evaluate(parse(expression), env)
    assert evaluate(parse("(count 0 (list 0 1 2 3 0 0))"), env) == 3

    expression = "(count (quote the) (quote (the more the merrier the bigger the better)))"
    assert evaluate(parse(expression), env) == 4


def test_evaluate_repeat():
    env = standard_env()
    evaluate(parse("(define twice (lambda (x) (* 2 x)))"), env)
    assert evaluate(parse("(twice 5)"), env) == 10

    evaluate(parse("(define repeat (lambda (f) (lambda (x) (f (f x)))))"), env)
    assert evaluate(parse("((repeat twice) 10)"), env) == 40
    assert evaluate(parse("((repeat (repeat twice)) 10)"), env) == 160
    assert evaluate(parse("((repeat (repeat (repeat twice))) 10)"), env) == 2560
    expression = "((repeat (repeat (repeat (repeat twice)))) 10)"
    assert evaluate(parse(expression), env) == 655360
    assert evaluate(parse("(pow 2 16)"), env) == 65536


def test_evaluate_fibonacci():
    env = standard_env()
    expression = "(define fib (lambda (n) (if (< n 2) 1 (+ (fib (- n 1)) (fib (- n 2))))))"
    evaluate(parse(expression), env)
    expression = "(define range (lambda (a b) (if (= a b) (quote ()) (cons a (range (+ a 1) b)))))"
    evaluate(parse(expression), env)
    assert evaluate(parse("(range 0 10)"), env) == list(range(10))

    assert [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] == list(
        evaluate(parse("(map fib (range 0 10))"), env),
    )
    assert [
        1,
        1,
        2,
        3,
        5,
        8,
        13,
        21,
        34,
        55,
        89,
        144,
        233,
        377,
        610,
        987,
        1597,
        2584,
        4181,
        6765,
    ] == list(evaluate(parse("(map fib (range 0 20))"), env))
