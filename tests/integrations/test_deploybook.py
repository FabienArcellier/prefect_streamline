import os
import sys

import pytest
from fixtup import fixtup
import requests

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..', '..', '..'))


@pytest.mark.filterwarnings("ignore:A flow named")
def test_deploy_should_list_deployments_of_flows_for_prefect():
    with fixtup.up('prefect'):
        with fixtup.up('fake_flow'):
            # We have to import the module after starting the environment
            # because Prefect will import the API url at the import
            # time. We need to set the environment variable before.
            from prefect_streamline import deploybook

            cwd = os.getcwd()
            sys.path.insert(0, cwd)
            deploybook.import_path(os.path.join(cwd, 'fake_flow.py'))

            # Acts
            deploybook.deploy()

            # Assert
            api_url = os.getenv('PREFECT_API_URL', 'http://localhost:42000/api')
            response = requests.post(f'{api_url}/deployments/filter', headers={
                'Content-Type': 'application/json',
            }, json={})
            deployments = response.json()
            assert len(deployments) == 2
            assert deployments[0]['entrypoint'] == 'fake_flow.py:myflow3'
            assert deployments[0]['path'] == os.getcwd()
            assert deployments[0]['name'] == 'hello2'
            assert deployments[1]['entrypoint'] == 'fake_flow.py:myflow3'
            assert deployments[1]['name'] == 'main'
