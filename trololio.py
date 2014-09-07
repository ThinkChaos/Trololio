from functools import wraps
from imp import find_module, load_module
from inspect import isgeneratorfunction
import os


__all__ = [
    'ASYNCIO', 'TROLLIUS', 'asyncio',
    'coroutine', 'From', 'Return',

    # OSError and socket.error exceptions
    'BlockingIOError', 'BrokenPipeError', 'ChildProcessError',
    'ConnectionAbortedError', 'ConnectionRefusedError', 'ConnectionResetError',
    'FileNotFoundError', 'InterruptedError', 'PermissionError',

    # SSLError
    'BACKPORT_SSL_ERRORS',
    'SSLEOFError', 'SSLWantReadError', 'SSLWantWriteError',

    # SSLContext
    'BACKPORT_SSL_CONTEXT',
    'SSLContext'
]


for _mod_name in ['trollius', 'asyncio']:
    try:
        _mod_file, _mod_pathname, _mod_description = find_module(_mod_name)
    except ImportError:
        asyncio = None
    else:
        ASYNCIO = _mod_name == 'asyncio'
        TROLLIUS = not ASYNCIO
        asyncio = load_module(
            'trololio.asyncio', _mod_file,
            _mod_pathname, _mod_description
        )
        break

if asyncio is None:
    # Generate a nice traceback
    import trollius


_asyncio_debug = os.environ.get('PYTHONASYNCIODEBUG') in ['0', '1']
_trollius_debug = os.environ.get('TROLLIUSDEBUG') in ['0', '1']

if _asyncio_debug and not _trollius_debug:
    os.environ['TROLLIUSDEBUG'] = os.environ['PYTHONASYNCIODEBUG']
elif _trollius_debug and not _asyncio_debug:
    os.environ['PYTHONASYNCIODEBUG'] = os.environ['TROLLIUSDEBUG']


if TROLLIUS:
    from trololio.asyncio import (
        coroutine, From, Return,

        # OSError and socket.error exceptions
        BlockingIOError, BrokenPipeError, ChildProcessError,
        ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError,
        FileNotFoundError, InterruptedError, PermissionError,

        # SSLError
        BACKPORT_SSL_ERRORS,
        SSLEOFError, SSLWantReadError, SSLWantWriteError,

        # SSLContext
        BACKPORT_SSL_CONTEXT,
        SSLContext
    )

else:
    # trollius/coroutines.py
    def From(obj):
        return obj

    class Return(Exception):
        def __init__(self, *args):
            if not args:
                self.value = None
            elif len(args) == 1:
                self.value = args[0]
            else:
                self.value = args

    from builtins import (
        # OSError and socket.error exceptions
        BlockingIOError, BrokenPipeError, ChildProcessError,
        ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError,
        FileNotFoundError, InterruptedError, PermissionError,
    )

    BACKPORT_SSL_CONTEXT = False
    BACKPORT_SSL_ERRORS = False

    from ssl import (
        # SSLError
        SSLEOFError, SSLWantReadError, SSLWantWriteError,

        # SSLContext
        SSLContext
    )

    from textwrap import dedent

    # exec is required because of `yield from` SyntaxError in Py2
    # exec on definition instead of on every yield for less overhead
    exec(dedent(
        """
        def coroutine(func):
            if not isgeneratorfunction(func):
                coro = asyncio.coroutine(func)
            else:
                @wraps(func)
                def coro(*args, **kwargs):
                    gen = func(*args, **kwargs)

                    for coro_or_fut in gen:
                        res = yield from coro_or_fut
                        gen.send(res)

            @wraps(coro)
            def return_handler(*args, **kwargs):
                try:
                    res = yield from coro(*args, **kwargs)
                except Return as res:
                    return res.value
                else:
                    return res

            return asyncio.coroutine(return_handler)
        """
    ))

    del dedent

del (
    find_module, load_module, os,
    _mod_description, _mod_file, _mod_name, _mod_pathname,
    _asyncio_debug, _trollius_debug
)
