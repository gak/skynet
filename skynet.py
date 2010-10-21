#!/usr/bin/env python

import pprint
import random
import ast

import codegen

module = ast.Module()
module.body = []

class Skynet:

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

    def random_var(self):
        return ast.Name(id='a')

    def random_var_store(self):
        v = self.random_var()
        v.ctx = ast.Store()
        return v

    def random_var_load(self):
        v = self.random_var()
        v.ctx = ast.Load()
        return v

    def random_func_name(self):
        return 'func%i' % random.randint(0, 3)

    def random_func_var(self):
        n = self.random_func_name()
        return ast.Name(id=n, ctx=ast.Load())

    def random_state(self):
        r = random.randint(0, 3)
        if r == 0:
            print 'print expr'
            return ast.Print(values=[self.random_expr()], nl=True, dest=None)
        if r == 1:
            print 'assign'
            return ast.Assign(targets=[self.random_var_store()], value=self.random_expr())
        if r == 2:
            print 'def'
            body = []
            self.add_random_code(body, 2)
            return ast.FunctionDef(body=body, decorator_list=[],
                    name=self.random_func_name(),
                    args=ast.arguments(args=[], kwarg=None, defaults=[],
                        vararg=None))
        if r == 3:
            print 'call'
            c = ast.Call(func=self.random_func_var(), args=[], keywords=[], starargs=None, kwargs=None)
            return ast.Expr(value=c)

    def random_expr(self):
        r = random.randint(0, 2)
        if r == 0:
            print 'num'
            return ast.Num(n=random.randint(0, 10))
        if r == 1:
            print 'binop'
            return ast.BinOp(
                left=self.random_expr(),
                op=self.random_op(),
                right=self.random_expr())
        if r == 2:
            print 'var'
            return self.random_var_load()

    def add_random_code(self, body, count=10):
        for a in xrange(count):
            body.append(self.random_state())

    def main(self):
        self.add_random_code(module.body)

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

Skynet().main()

