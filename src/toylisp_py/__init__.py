"""A simple Lisp interpreter inspired by "How to Write a (Lisp) Interpreter (in Python)" by Peter Norvig."""

from .lisp import repl


def main():
    """Execute the script. Launch a REPL of toylisp interpreter."""
    repl()
