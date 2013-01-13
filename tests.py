# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chut.recipe import Recipe
from chut.scripts import chutify
import chut as sh
import unittest
import six
import os


class Chut(unittest.TestCase):

    __file__ = __file__.replace('.pyc', '.py')

    def test_output(self):
        self.assertEqual(sh.rm('/chut').succeeded, False)
        self.assertEqual(sh.rm('/chut').failed, True)
        self.assertTrue(len(sh.rm('/chut').stderr) >= 0)

    def test_repr(self):
        self.assertEqual(repr(sh.stdin(six.b('')) | sh.cat('-')),
                         repr(str('stdin | cat -')))

        @sh.wraps
        def w():
            pass

        self.assertEqual(repr(sh.cat('-') | w),
                         repr(str('cat - | w()')))

    def test_environ(self):
        env = sh.env(tmp='tmp')
        self.assertEqual(env.tmp, 'tmp')

    def test_slices(self):
        pipe = sh.cat('tmp') | sh.grep('tmp') | sh.wc('-l')
        self.assertEqual(pipe[0:1]._binary, 'cat')
        self.assertEqual(pipe.__getitem__(slice(0, 1))._binary, 'cat')
        self.assertEqual(pipe.__getslice__(0, 1)._binary, 'cat')
        self.assertEqual(pipe[1:]._binary, 'wc')
        self.assertEqual(pipe.__getitem__(slice(1, 3))._binary, 'wc')
        self.assertEqual(pipe.__getslice__(1, 3)._binary, 'wc')

        self.assertRaises(KeyError, pipe.__getitem__, 1)

    def test_redirect_binary(self):
        with sh.pipes(sh.cat(__file__)) as cmd:
            cmd > 'tmp'
        ls = str(sh.ls('-l tmp'))

        with sh.pipes(sh.cat(__file__)) as cmd:
            cmd >> 'tmp'
        self.assertFalse(ls == str(sh.ls('-l tmp')))
        sh.rm('tmp')

    def test_redirect_python(self):

        @sh.wraps
        def grep(stdin):
            for line in stdin:
                if b'__' in line:
                    yield line

        pipe = sh.cat(__file__) | grep
        with sh.pipes(pipe) as cmd:
            cmd > 'tmp'
        ls = str(sh.ls('-l tmp'))
        with sh.pipes(pipe) as cmd:
            cmd >> 'tmp'
        self.assertFalse(ls == str(sh.ls('-l tmp')), ls)

    def test_stdin(self):
        content = open(__file__).read().strip()
        if not isinstance(content, six.binary_type):
            bcontent = content.encode('utf-8')
        else:
            bcontent = content
        self.assertEqual(content,
                         str(sh.stdin(bcontent) | sh.cat('-')))
        self.assertEqual(content,
                         str(sh.stdin(open(__file__, 'rb')) | sh.cat('-')))

    def test_redirect_stdin(self):
        sh.stdin(b'blah') > 'tmp'
        self.assertEqual(str(sh.cat('tmp')), 'blah')

        sh.stdin(b'blah') >> 'tmp'
        self.assertEqual(str(sh.cat('tmp')), 'blahblah')

    def test_stdin2(self):
        head = str(sh.stdin(open(self.__file__, 'rb'))
                   | sh.cat('-')
                   | sh.head('-n1'))
        self.assertTrue(len(head) > 1, head)
        self.assertTrue(len(head) > 2, head)

    def test_raise(self):
        self.assertRaises(OSError, str, sh.zero_command())

    def test_sudo(self):
        sh.aliases['sudo'] = sh.path.join(sh.pwd(), 'sudo')
        old_path = sh.env.path
        sh.env.path = []
        self.assertRaises(OSError, sh.check_sudo)
        sh.env.path = old_path

        sh.stdin(six.b('#!/bin/bash\necho root')) > 'sudo'
        self.assertEqual(sh.chmod('+x sudo').succeeded, True)
        self.assertEqual(sh.check_sudo(), None)

        self.assertTrue(len(list(sh.sudo.ls('.'))) > 0)

        sh.stdin(six.b('#!/bin/bash\necho gawel')) > 'sudo'
        self.assertRaises(OSError, sh.check_sudo)

    def test_cd(self):
        pwd = sh.pwd()
        sh.cd('..')
        self.assertNotEqual(pwd, sh.env.pwd)
        self.assertEqual(sh.pwd(), sh.env.pwd)
        sh.cd(pwd)

    def test_console_script(self):
        def f(args):
            return 1
        f = sh.console_script(f)
        self.assertRaises(SystemExit, f)
        self.assertEqual(f([]), 1)

    def test_generate(self):
        self.assertEqual(sh.generate('chut/scripts.py'), 0)

    def test_chutify(self):
        self.assertEqual(chutify(['chut/scripts.py']), 0)
        self.assertEqual(chutify(['.']), 0)
        self.assertEqual(chutify(['.', '-l']), 0)

    def test_recipe(self):
        r = Recipe({'buildout': {'directory': os.getcwd()}},
                    'chut', {'destination': 'dist/scripts',
                             'run': 'ls\nls .\n '})
        self.assertEqual(r.install(), ())
        r = Recipe({'buildout': {'directory': os.getcwd()}},
                    'chut', {'destination': 'dist/scripts'})
        self.assertEqual(r.update(), ())

    def test_map(self):
        self.assertRaises(OSError, list,
                          sh.rm.map(['/chut'], stop_on_failure=True))

    def test_call_opts(self):
        self.assertEqual(str(sh.ls('.')), str(sh.ls('.', shell=True)))
        self.assertEqual(str(sh.ls('.')), str(sh.ls('.')(shell=True)))
        self.assertEqual(str(sh.ls('.')), str(sh.ls('.', combine_stderr=True)))
        self.assertEqual(str(sh.ls('.')), str(sh.ls('.')(combine_stderr=True)))

    def tearDown(self):
        sh.rm('-f tmp')
        sh.rm('-f sudo')
