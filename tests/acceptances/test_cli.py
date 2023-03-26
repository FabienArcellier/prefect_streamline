import contextlib
import os

import pytest
from fixtup import fixtup

from prefect_streamline.cli import cli
from click.testing import CliRunner

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..', '..', '..'))


@pytest.mark.filterwarnings("ignore:A flow named")
def test_deploy_should_list_deployments_of_flows():
    with fixtup.up('fake_flow'):
        cwd = os.getcwd()
        runner = CliRunner()

        result = runner.invoke(cli, ['deploy', '-l', os.path.join(cwd, 'fake_flow.py')])
        assert result.exit_code == 0
        assert 'myflow3 (name:main, interval:60)\n' in result.output


@pytest.mark.filterwarnings("ignore:A flow named")
def test_deploy_should_discover_deployments_of_flows():
    with fixtup.up('fake_flow'):
        cwd = os.getcwd()
        runner = CliRunner()

        result = runner.invoke(cli, ['deploy', '-l', '--discover', cwd])
        assert result.exit_code == 0
        assert 'myflow3 (name:main, interval:60)\n' in result.output



