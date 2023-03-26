from typing import Optional

import click
from click import UsageError

from prefect_streamline import deploybook

@click.group()
def cli():
    pass


@cli.command('deploy')
@click.option('--discover', '-d', is_flag=True, help='discover flows in all submodules')
@click.option('--list', '-l', '_list', is_flag=True, help='list all the deployments', metavar='list_')
@click.option('--module', '-m', help='module to look flows in')
@click.argument('path', nargs=1, required=False)
def deploy_cmd(discover: bool, _list: bool, module: Optional[str] = None, path: Optional[str] = None):
    """
    deploy will deploy flow to prefect register with deploybook.register.

    \b
    $ prefect_streamline deploy src/app/flow.py
    $ prefect_streamline deploy -d src/app

    deploy can use module instead of path.

    \b
    $ prefect_streamline deploy -m app.flow
    """
    from prefect_streamline.core import deploy

    if module is None and path is None:
        raise UsageError(f"either module or or path must be defined")

    if module is not None and path is not None:
        raise UsageError(f"either module or or path must be defined, not both")

    if module is not None and discover is True:
        _echo_warning("option --discover/-d is not compatible with option --module/-m")

    if module is not None:
        deploybook.import_module(module)

    if path is not None:
        deploybook.import_path(path, discover=discover)

    if _list is False:
        deploybook.deploy()
    else:
        deploys = deploybook.list()
        for _deploy in deploys:
            click.echo(_deploy.format())


def _echo_warning(text: str) -> None:
    click.echo(click.style(f"Warning: {text}", fg='yellow'))
