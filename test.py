from trololio import asyncio, coroutine, From, Return


@coroutine
def coro_ret(*args):
    raise Return(*args)


@coroutine
def coro_yield(sleep_time):
    yield From(asyncio.sleep(sleep_time))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        for x in ([1, 2, 3], None, [None]):
            res = loop.run_until_complete(coro_ret(x))
            assert res == x

        loop.run_until_complete(coro_yield(1))
    finally:
        loop.close()
