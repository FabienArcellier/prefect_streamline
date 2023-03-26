import time
from time import monotonic
from typing import Optional

import requests


def request_ok(url: str, timeout: Optional[int] = None, attempt_every: int = 1000) -> None:
    """
    wait until a url reply to http request with 200.

    >>> fixtup.helper.base.request_ok(
    >>>         'http://localhost:9000/probes/readz',
    >>>         timeout=5000)

    :param url: port that has to be open
    :param timeout: timeout in ms before raising TimeoutError.
    """
    start = monotonic()
    ready = False
    while ready is False and (timeout is None or monotonic() - start < timeout / 1000):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                ready = True
                break
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(attempt_every / 1000)

    if ready is False:
        raise TimeoutError(f"{url} is not ready after {timeout}ms")

    return
