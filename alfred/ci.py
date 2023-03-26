import os

import alfred
import click

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("ci", help="workflow to execute the continuous integration process")
def ci():
    """
    workflow to execute the continuous integration process

    * run the linter
    * run the automated tests beginning with units tests

    >>> $ alfred ci
    """
    alfred.invoke_command('lint')
    alfred.invoke_command('tests')


@alfred.command("ci:regression", help="execute integrations tests")
@click.option('--prefect', '-p', help='version to test prefect with')
def ci__regressions(prefect):
    """

    >>> $ alfred ci:regression -p 2.6
    """
    poetry = alfred.sh("poetry")
    os.chdir(ROOT_DIR)
    alfred.run(poetry, ['add', f'prefect=~{prefect}'])

    os.chdir(os.path.join(ROOT_DIR, 'tests', 'fixture', 'prefect'))
    alfred.run(poetry, ['add', f'prefect==~{prefect}'])

    alfred.invoke_command('tests')
