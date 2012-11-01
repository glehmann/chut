Internals
==========

Pipe
====

.. autoclass:: chut.Pipe
   :members:

..
    >>> import chut as sh
    >>> from chut import cat, grep

Input
=====

You can use a python string as input::

    >>> print(sh.stdin(b'gawel\nfoo') | grep('gawel'))
    gawel

The input can be a file but the file is not streamed by ``stdin()``.
Notice that the file must be open in binary mode (``rb``)::

    >>> print(sh.stdin(open('README.rst', 'rb'))
    ...               | grep('Chut') | sh.head('-n1'))
    Chut!

.. autoclass:: chut.Stdin
   :members:

Output
======

You can get the output as string (see :class:`~chut.Stdout`)::

    >>> output = str(cat('README.rst') | grep('Chut'))
    >>> output = (cat('README.rst') | grep('Chut'))()

As an iterator (iterate over each lines of the output)::

    >>> chut_stdout = cat('README.rst') | grep('Chut') | sh.head('-n1')

And can use some redirection::

    >>> ret = chut_stdout > '/tmp/chut.txt'
    >>> ret.succeeded
    True
    >>> print(cat('/tmp/chut.txt'))
    Chut!

    >>> ret = chut_stdout >> '/tmp/chut.txt'
    >>> ret.succeeded
    True
    >>> print(cat('/tmp/chut.txt'))
    Chut!
    Chut!

Parentheses are needed with ``>>`` (due to the way the python operator work)::

    cat('README.rst') | grep >> '/tmp/chut.txt' # wont work
    (cat('README.rst') | grep) >> '/tmp/chut.txt' # work

.. autoclass:: chut.Stdout
   :members: