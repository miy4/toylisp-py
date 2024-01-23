# toylisp-py

A simple Lisp interpreter inspired by [(How to Write a (Lisp) Interpreter (in Python))](http://norvig.com/lispy.html) by Peter Norvig. The primary objective here is to explore Python programming concepts by implementing a functional Lisp interpreter.

## Examples and Usage

Here are some examples of how to use the Lisp interpreter on the REPL:

```shell-session
$ rye sync
...
$ rye run repl
lis.py> (+ 1 2)
3
lis.py> (define r 10)
lis.py> (print r)
10
lis.py> (begin (define square (lambda (x) (* x x))) (square 5))
25
```

