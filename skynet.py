#!/usr/bin/env python

import pprint
import random
import ast

import codegen

module = ast.Module()
module.body = []

def random_op():
    r = random.randint(0, 3)
    if r == 0:
        return ast.Add()
    if r == 1:
        return ast.Sub()
    if r == 2:
        return ast.Mult()
    if r == 3:
        return ast.Div()

def random_var():
    return ast.Name(id='a')

def random_var_store():
    v = random_var()
    v.ctx = ast.Store()
    return v

def random_var_load():
    v = random_var()
    v.ctx = ast.Load()
    return v

def random_func_name():
    return 'func%i' % random.randint(0, 3)

def random_func_var():
    n = random_func_name()
    return ast.Name(id=n, ctx=ast.Load())

def random_state():
    r = random.randint(0, 3)
    if r == 0:
        print 'print expr'
        return ast.Print(values=[random_expr()], nl=True, dest=None)
    if r == 1:
        print 'assign'
        return ast.Assign(targets=[random_var_store()], value=random_expr())
    if r == 2:
        print 'def'
        body = []
        add_random_code(body, 2)
        return ast.FunctionDef(body=body, decorator_list=[],
                name=random_func_name(),
                args=ast.arguments(args=[], kwarg=None, defaults=[],
                    vararg=None))
    if r == 3:
        print 'call'
        c = ast.Call(func=random_func_var(), args=[], keywords=[], starargs=None, kwargs=None)
        return ast.Expr(value=c)

def random_expr():
    r = random.randint(0, 2)
    if r == 0:
        print 'num'
        return ast.Num(n=random.randint(0, 10))
    if r == 1:
        print 'binop'
        return ast.BinOp(
            left=random_expr(),
            op=random_op(),
            right=random_expr())
    if r == 2:
        print 'var'
        return random_var_load()

def add_random_code(body, count=10):
    for a in xrange(count):
        body.append(random_state())

add_random_code(module.body)

ast.fix_missing_locations(module)

print '-' * 80
print 'code:'
print '-' * 80,
from unparse import Unparser
up = Unparser(module)

print
print '-' * 80
print 'output:'
print '-' * 80
exec(compile(module, '<string>', 'exec'))

