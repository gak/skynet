#!/usr/bin/env python
from __future__ import division

import random
import ast

import codegen

class Skynet:

    def __init__(self):
        self.attempts = 0
        self.success = 0
        self.reset()

    def reset(self):
        self.func_depth = 0
        self.vars = {
            'var': [],
            'fun': [],
        }

    def generate(self):
        self.reset()
        module = ast.Module()
        module.body = []
        self.add_random_code(module.body)
        ast.fix_missing_locations(module)

        if 0:
            print ast.dump(module)

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

    def random_var_name(self, prefix, range, existing):
        if existing:
            try:
                return random.choice(self.vars[prefix])
            except IndexError:
                return
        else:
            r = random.randint(0, range)
            c = chr(ord('a') + r)
            n = prefix + '_' + c
            self.vars[prefix].append(n)
            return n

    def random_var(self, existing):
        n = self.random_var_name('var', 3, existing)
        if not n:
            return
        return ast.Name(id=n)

    def random_var_store(self):
        v = self.random_var(existing=False)
        v.ctx = ast.Store()
        return v

    def random_var_load(self):
        v = self.random_var(existing=True)
        if not v:
            return
        v.ctx = ast.Load()
        return v

    def random_func_name(self, existing=False):
        return self.random_var_name('fun', 3, existing)

    def random_func_var(self):
        n = self.random_func_name(existing=True)
        if not n:
            return
        return ast.Name(id=n, ctx=ast.Load())

    def random_call(self):
        func = self.random_func_var()
        if not func:
            return
        return ast.Call(func=func,
            args=[], keywords=[], starargs=None, kwargs=None)

    def random_state(self):
        r = random.randint(0, 4)
        if r == 0:
            var = self.random_expr()
            if not var:
                return
            return ast.Print(values=[var], nl=True, dest=None)
        if r == 1:
            var = self.random_expr()
            if not var:
                return
            return ast.Assign(
                targets=[self.random_var_store()],
                value=var)
        if r == 2:
            if self.func_depth > 0:
                return
            func_name = self.random_func_name()
            if not func_name:
                return
            self.func_depth += 1
            body = []
            self.add_random_code(body)
            if not len(body):
                self.func_depth -= 1
                return
            f = ast.FunctionDef(body=body, decorator_list=[],
                    name=func_name,
                    args=ast.arguments(args=[], kwarg=None, defaults=[],
                        vararg=None))
            self.func_depth -= 1
            return f
        if r == 3:
            c = self.random_call()
            if not c:
                return
            return ast.Expr(value=c)
        if r == 4:
            if self.func_depth == 0:
                return
            var = self.random_expr()
            if not var:
                return
            return ast.Return(value=var)

    def random_expr(self):
        r = random.randint(0, 3)
        if r == 0:
            return ast.Num(n=random.randint(0, 10))
        if r == 1:
            left = self.random_expr()
            right = self.random_expr()
            if not left or not right:
                return
            return ast.BinOp(
                left=left,
                op=self.random_op(),
                right=right
                )
        if r == 2:
            var = self.random_var_load()
            if not var:
                return
            return var
        if r == 3:
            return self.random_call()

    def add_random_code(self, body, count=20):
        for a in xrange(count):
            statement = self.random_state()
            if not statement:
                continue
            body.append(statement)

Skynet().main()

