"""
This module provides a library to plan a deployment for Prefect.
The developer saves these flows in a deployment book.

>>> deploy_book = deploy.create_deploy_book()
>>> deploy.register(deploy_book, flow1)
>>> deploy.register(deploy_book, flow2)
>>> deploy.deploy(deploy_book)
"""
import dataclasses
import os
from datetime import timedelta
from typing import List, Optional, cast

from prefect import Flow
from prefect.schedules import Schedule
from prefect.types.entrypoint import EntrypointType

from prefect_streamline.core import waiting


@dataclasses.dataclass
class DeployFlow:
    """
    defines a flow to deploy
    """
    flow: Flow
    name: Optional[str] = None
    interval: Optional[int] = None
    cron: Optional[str] = None
    work_pool_name: Optional[str] = None
    work_queue_name: Optional[str] = None

    def __post_init__(self):
        if self.name is None:
            self.name = "main"

    @property
    def schedule(self) -> Optional[Schedule]:
        if self.interval is None and self.cron is None:
            return None
        elif self.interval is not None:
            return Schedule(interval=timedelta(seconds=self.interval))
        elif self.cron is not None:
            return Schedule(cron=self.cron)

        return None

    def format(self):
        label = f"{self.flow.__name__}" + " ("
        elements = []
        if self.name is not None:
            elements.append(f"name:{self.name}")
        if self.interval is not None:
            elements.append(f"interval:{self.interval}")
        if self.cron is not None:
            elements.append(f"cron:{self.cron}")

        return label + ", ".join(elements) + ")"


@dataclasses.dataclass
class DeployBook:
    deploy_flows: List[DeployFlow] = dataclasses.field(default_factory=list)


def create_deploy_book() -> DeployBook:
    return DeployBook()


def register(deploy_book: DeployBook, flow: Flow, name: Optional[str] = None, interval: Optional[int] = None,
             cron: Optional[str] = None, work_pool_name: Optional[str] = None, work_queue_name: Optional[str] = None) -> None:
    if interval is not None and cron is not None:
        raise ValueError(f"Cannot define both interval and cron for the flow {flow.name=} - {interval=} - {cron=}")

    if not isinstance(flow, Flow):
        raise ValueError(
            f"Cannot register {flow} as it is not a Flow, maybe you set deploybook.register first instead of flow")

    deploy_book.deploy_flows.append(
        DeployFlow(flow=flow, name=name, interval=interval, cron=cron, work_pool_name=work_pool_name, work_queue_name=work_queue_name))


def deploy(book: DeployBook, timeout: int = 60000) -> None:
    """
    The url of the prefect instance to deploy to is retrieved
    from the PREFECT_API_URL environment variable

    Inject a specific PREFECT_API_URL variable of the endpoint the deploy script will use.
    """
    api_url = os.getenv('PREFECT_API_URL')
    waiting.request_ok(f"{api_url}/health", timeout=timeout)

    for deploy_flow in book.deploy_flows:
        schedules = [deploy_flow.schedule] if deploy_flow.schedule else None
        deployment = deploy_flow.flow.to_deployment(
            name=cast(str, deploy_flow.name),
            schedules=schedules,
            entrypoint_type=EntrypointType.MODULE_PATH,
            work_pool_name=deploy_flow.work_pool_name,
            work_queue_name=deploy_flow.work_queue_name
        )

        deployment.apply()  # type: ignore


def deployment_list(book: DeployBook):
    return book.deploy_flows
