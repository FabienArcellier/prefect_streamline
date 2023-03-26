import contextlib
from typing import Optional, List

from prefect_streamline.core import deploy as core_deploy, importutils

_deploy_book = core_deploy.DeployBook()


def deploy() -> None:
    core_deploy.deploy(_deploy_book)


def list() -> List[core_deploy.DeployFlow]:
    return core_deploy.list(_deploy_book)


def register(name: Optional[str] = None, interval: Optional[int] = None, cron: Optional[str] = None):
    """
    register a flow to deploy it with the command prefect-streamline deploy

    >>> from prefect import flow
    >>> from prefect_streamline import deploybook
    >>>
    >>> @deploybook.register(interval=60)
    >>> @flow(name="main.my_favorite_function")
    >>> def myflow() -> int:
    >>>     return 43

    it is possible to save several deployments for the same flow.

    >>> from prefect import flow
    >>> from prefect_streamline import deploybook
    >>>
    >>> @deploybook.register(interval=60)
    >>> @deploybook.register(interval=3600, name="daily")
    >>> @flow(name="main.myflow")
    >>> def myflow() -> int:
    >>>     return 43

    it is possible to use a cron expression instead of an interval but not both at the same time in the same record.

    >>> from prefect import flow
    >>> from prefect_streamline import deploybook
    >>>
    >>> @deploybook.register(interval=60)
    >>> @deploybook.register(cron="0 0 * * *", name="daily")
    >>> @flow(name="main.myflow")
    >>> def myflow() -> int:
    >>>     return 43
    """

    def inner(func):
        core_deploy.register(_deploy_book, func, name=name, interval=interval, cron=cron)
        return func

    return inner


@contextlib.contextmanager
def use_dedicated_deploybook():
    global _deploy_book
    current_deploy_book = _deploy_book
    _deploy_book = core_deploy.DeployBook()
    yield
    _deploy_book = current_deploy_book


def import_module(module: str) -> None:
    importutils.import_module(module)


def import_path(path: str, discover: bool = False) -> None:
    importutils.import_path(path, discover)
