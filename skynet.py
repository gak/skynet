#!/usr/bin/env python
from __future__ import division

import random
import ast

import codegen

class Skynet:

    def __init__(self):
        self.attempts = 0
        self.success = 0
        self.func_depth = 0

    def generate(self):
        module = ast.Module()
        module.body = []
        self.add_random_code(module.body)
        ast.fix_missing_locations(module)

        if 1:
            print '-' * 80
            print 'code:'
            print '-' * 80,
            from unparse import Unparser
            up = Unparser(module)

        if 1:
            print
            print '-' * 80
            print 'output:'
            print '-' * 80

        self.attempts += 1
        try:
            exec(compile(module, '<string>', 'exec'))
            self.success += 1
            raw_input()
        except Exception, e:
            print e

    def main(self):
        while 1:
            self.generate()
            
    def random_op(self):
        r = random.randint(0, 3)
        if r == 0:
            return ast.Add()
        if r == 1:
            return ast.Sub()
        if r == 2:
            return ast.Mult()
        if r == 3:
            return ast.Div()

    def random_var_name(self, prefix, range):
        r = random.randint(0, range)
        c = chr(ord('a') + r)
        return prefix + '_' + c

    def random_func_name(self):
        return self.random_var_name('fun', 3)

    def random_var(self):
        return ast.Name(id=self.random_var_name('var', 3))

    def random_var_store(self):
        v = self.random_var()
        v.ctx = ast.Store()
        return v

    def random_var_load(self):
        v = self.random_var()
        v.ctx = ast.Load()
        return v

    def random_func_var(self):
        n = self.random_func_name()
        return ast.Name(id=n, ctx=ast.Load())

    def random_call(self):
        return ast.Call(func=self.random_func_var(), args=[], keywords=[], starargs=None, kwargs=None)

    def random_state(self):
        r = random.randint(0, 4)
        if r == 0:
            return ast.Print(values=[self.random_expr()], nl=True, dest=None)
        if r == 1:
            return ast.Assign(targets=[self.random_var_store()], value=self.random_expr())
        if r == 2:
            if self.func_depth > 0:
                return ast.Pass()
            self.func_depth += 1
            body = []
            self.add_random_code(body, 5)
            f = ast.FunctionDef(body=body, decorator_list=[],
                    name=self.random_func_name(),
                    args=ast.arguments(args=[], kwarg=None, defaults=[],
                        vararg=None))
            self.func_depth -= 1
            return f
        if r == 3:
            c = self.random_call()
            return ast.Expr(value=c)
        if r == 4:
            if self.func_depth == 0:
                return ast.Pass()
            return ast.Return(value=self.random_expr())

    def random_expr(self):
        r = random.randint(0, 3)
        if r == 0:
            return ast.Num(n=random.randint(0, 10))
        if r == 1:
            return ast.BinOp(
                left=self.random_expr(),
                op=self.random_op(),
                right=self.random_expr())
        if r == 2:
            return self.random_var_load()
        if r == 3:
            return self.random_call()

    def add_random_code(self, body, count=5):
        for a in xrange(count):
            body.append(self.random_state())

Skynet().main()

