#!/usr/bin/env python
from __future__ import division

import sys
import random
import ast
import cStringIO as StringIO

import codegen

class Skynet:

    def __init__(self):
        self.attempts = 0
        self.success = 0
        self.best = 0

    def run(self, app):
        module = app.generate()
        self.attempts += 1

        s = StringIO.StringIO()
        sys.stdout = s
        try:
            exec(compile(module, '<string>', 'exec'))
            self.success += 1
            fail = False
        except Exception, e:
            fail = True
            print e
        sys.stdout = sys.__stdout__

        values = s.getvalue().split()
        total = 0
        for v in values:
            try:
                v = float(v)
            except:
                continue
            total += v
        score = total * len(set(values))
        if score > self.best:
            self.best = score
        
        app.dump_code(module)
        print values, score
        raw_input('? ')

        if fail:
            return

    def main(self):
        while 1:
            app = SkynetApp()
            self.run(app)
           

class SkynetApp:
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.func_depth = 0
        self.loop_depth = 0
        self.vars = {
            'var': [],
            'fun': [],
        }

    def generate(self):
        self.reset()
        module = ast.Module()
        module.body = []
        module.body = self.random_body()
        ast.fix_missing_locations(module)
        return module

    def dump_module(self, module):
        print ast.dump(module)

    def dump_code(self, module):
        print '-' * 80
        print 'code:'
        print '-' * 80,
        from unparse import Unparser
        up = Unparser(module)
        print

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
        r = random.randint(0, 5)
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
            body = self.random_body()
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
        if r == 5:
            if self.loop_depth > 2:
                return
            self.loop_depth += 1
            iter = self.random_iter()
            if not iter:
                self.loop_depth -= 1
                return
            var = self.random_var_store()
            body = self.random_body()
            if not body:
                self.loop_depth -= 1
                return
            f = ast.For(target=var, iter=iter, body=body, orelse=[])
            self.loop_depth -= 1
            return f
        if r == 6:
            return self.random_cond()

    def random_expr(self):
        r = random.randint(0, 2)
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

    def random_cond(self):
        var1 = self.random_expr()
        if not var1:
            return
        var2 = self.random_expr()
        if not var2:
            return
        body = self.random_body()
        if not body:
            return
        elsebody = self.random_body()
        if not elsebody:
            return
        cmp = random.choice([ast.Eq(), ast.Gt(), ast.Lt()])
        return ast.If(ast.Compare(left=var1, comparators=[var2], ops=cmp,
                body=body, orelse=elsebody))

    def random_iter(self):
        r = random.randint(1, 10)
        return ast.Call(func=ast.Name(id='range', ctx=ast.Load()), args=[ast.Num(n=r)],
            keywords=[], starargs=None, kwargs=None)

    def random_body(self, count=5):
        body = []
        for a in xrange(count):
            statement = self.random_state()
            if not statement:
                continue
            body.append(statement)
        return body

Skynet().main()

