"""
Ce module fournit quelques primitives pour tester des taches depuis prefect
"""
import contextlib
import logging
from typing import Any, TypeVar
from typing_extensions import ParamSpec

from prefect import Flow

R = TypeVar('R')
P = ParamSpec('P')


@contextlib.contextmanager
def use_native_runner():
    """
    Hack prefect to run a flow as a native python function for testing.

    * Disable prefect logging for test execution, it is useful when fn is used

    >>> with use_native_runner():
    >>>    fn(my_favorite_function)(42)
    """
    flow_run_initial_state = logging.getLogger("prefect.flow_run").disabled
    task_run_initial_state = logging.getLogger("prefect.task_run").disabled

    logging.getLogger("prefect.flow_run").disabled = True
    logging.getLogger("prefect.task_run").disabled = True
    try:
        yield
    finally:
        logging.getLogger("prefect.flow_run").disabled = flow_run_initial_state
        logging.getLogger("prefect.task_run").disabled = task_run_initial_state


def fn(flow: Flow, *args, **kwargs) -> Any:
    """
    Execute a flow with the given arguments bypassing the overhead of prefect.

    >>> flow(my_favorite_function)(42)
    """

    return flow.fn  # type: ignore[attr-defined]

