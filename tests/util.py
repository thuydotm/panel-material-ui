from __future__ import annotations

import asyncio
import platform
import re
import socket
import sys
import time
import uuid

import pytest
import requests

from packaging.version import Version

import panel as pn

from panel.io.server import serve
from panel.io.state import state

# Ignore tests which are not yet working with Bokeh 3.
# Will begin to fail again when the first rc is released.
pnv = Version(pn.__version__)

APP_PATTERN = re.compile(r'Bokeh app running at: http://localhost:(\d+)/')
ON_POSIX = 'posix' in sys.builtin_module_names

linux_only = pytest.mark.skipif(platform.system() != 'Linux', reason="Only supported on Linux")
unix_only = pytest.mark.skipif(platform.system() == 'Windows', reason="Only supported on unix-like systems")


def wait_until(fn, page=None, timeout=5000, interval=100):
    """
    Exercise a test function in a loop until it evaluates to True
    or times out.

    The function can either be a simple lambda that returns True or False:
    >>> wait_until(lambda: x.values() == ['x'])

    Or a defined function with an assert:
    >>> def _()
    >>>    assert x.values() == ['x']
    >>> wait_until(_)

    In a Playwright context test you should pass the page fixture:
    >>> wait_until(lambda: x.values() == ['x'], page)

    Parameters
    ----------
    fn : callable
        Callback
    page : playwright.sync_api.Page, optional
        Playwright page
    timeout : int, optional
        Total timeout in milliseconds, by default 5000
    interval : int, optional
        Waiting interval, by default 100

    Adapted from pytest-qt.
    """
    # Hide this function traceback from the pytest output if the test fails
    __tracebackhide__ = True

    start = time.time()

    def timed_out():
        elapsed = time.time() - start
        elapsed_ms = elapsed * 1000
        return elapsed_ms > timeout

    timeout_msg = f"wait_until timed out in {timeout} milliseconds"

    while True:
        try:
            result = fn()
        except AssertionError as e:
            if timed_out():
                raise TimeoutError(f"{timeout_msg}: {e}") from e
        else:
            if result not in (None, True, False):
                raise ValueError(
                    "`wait_until` callback must return None, True or "
                    f"False, returned {result!r}"
                )
            # None is returned when the function has an assert
            if result is None:
                return
            # When the function returns True or False
            if result:
                return
            if timed_out():
                raise TimeoutError(timeout_msg)
        if page:
            # Playwright recommends against using time.sleep
            # https://playwright.dev/python/docs/intro#timesleep-leads-to-outdated-state
            page.wait_for_timeout(interval)
        else:
            time.sleep(interval / 1000)


async def async_wait_until(fn, page=None, timeout=5000, interval=100):
    """
    Exercise a test function in a loop until it evaluates to True
    or times out.

    The function can either be a simple lambda that returns True or False:
    >>> await async_wait_until(lambda: x.values() == ['x'])

    Or a defined function with an assert:
    >>> async def _()
    >>>    assert x.values() == ['x']
    >>> await async_wait_until(_)

    In a Playwright context test, you should pass the page fixture:
    >>> await async_wait_until(lambda: x.values() == ['x'], page)

    Parameters
    ----------
    fn : callable
        Callback
    page : playwright.async_api.Page, optional
        Playwright page
    timeout : int, optional
        Total timeout in milliseconds, by default 5000
    interval : int, optional
        Waiting interval, by default 100

    Adapted from pytest-qt.
    """
    # Hide this function traceback from the pytest output if the test fails
    __tracebackhide__ = True

    start = time.time()

    def timed_out():
        elapsed = time.time() - start
        elapsed_ms = elapsed * 1000
        return elapsed_ms > timeout

    timeout_msg = f"async_wait_until timed out in {timeout} milliseconds"

    while True:
        try:
            result = fn()
            if asyncio.iscoroutine(result):
                result = await result
        except AssertionError as e:
            if timed_out():
                raise TimeoutError(timeout_msg) from e
        else:
            if result not in (None, True, False):
                raise ValueError(
                    "`async_wait_until` callback must return None, True, or "
                    f"False, returned {result!r}"
                )
            # None is returned when the function has an assert
            if result is None:
                return
            # When the function returns True or False
            if result:
                return
            if timed_out():
                raise TimeoutError(timeout_msg)
        if page:
            # Playwright recommends against using time.sleep
            # https://playwright.dev/python/docs/intro#timesleep-leads-to-outdated-state
            await page.wait_for_timeout(interval)
        else:
            await asyncio.sleep(interval / 1000)


def get_open_ports(n=1):
    sockets,ports = [], []
    for _ in range(n):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        ports.append(s.getsockname()[1])
        sockets.append(s)
    for s in sockets:
        s.close()
    return tuple(ports)


def serve_and_wait(app, page=None, prefix=None, port=None, **kwargs):
    server_id = kwargs.pop('server_id', uuid.uuid4().hex)
    if serve_and_wait.server_implementation == 'fastapi':
        from panel.io.fastapi import serve as serve_app
        port = port or get_open_ports()[0]
    else:
        serve_app = serve
    serve_app(app, port=port or 0, threaded=True, show=False, liveness=True, server_id=server_id, prefix=prefix or "", **kwargs)
    wait_until(lambda: server_id in state._servers, page)
    server = state._servers[server_id][0]
    if serve_and_wait.server_implementation == 'fastapi':
        port = port
    else:
        port = server.port
    wait_for_server(port, prefix=prefix)
    return port

serve_and_wait.server_implementation = 'tornado'

def serve_component(page, app, suffix='', wait=True, **kwargs):
    msgs = []
    page.on("console", lambda msg: msgs.append(msg))
    port = serve_and_wait(app, page, **kwargs)
    page.goto(f"http://localhost:{port}{suffix}")

    if wait:
        wait_until(lambda: any("Websocket connection 0 is now open" in str(msg) for msg in msgs), page, interval=10)

    return msgs, port


def wait_for_server(port, prefix=None, timeout=3):
    start = time.time()
    prefix = prefix or ""
    url = f"http://localhost:{port}{prefix}/liveness"
    while True:
        try:
            if requests.get(url).ok:
                return
        except Exception:
            pass
        time.sleep(0.05)
        if (time.time()-start) > timeout:
            raise RuntimeError(f'{url} did not respond before timeout.')
