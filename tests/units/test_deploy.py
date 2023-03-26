from prefect import flow

from prefect_streamline import deploybook


def test_register_should_register_a_flow_for_deployments():
    # Arrange
    with deploybook.use_dedicated_deploybook():
        @deploybook.register(interval=60)
        @flow()
        def myflow1() -> int:
            return 43

        assert len(deploybook._deploy_book.deploy_flows) == 1
        assert deploybook._deploy_book.deploy_flows[0].interval == 60


def test_register_should_register_a_flow_for_deployments_with_a_cron_expression():
    # Arrange
    with deploybook.use_dedicated_deploybook():
        @deploybook.register(cron="0 0 * * *")
        @flow()
        def myflow2() -> int:
            return 43

        assert len(deploybook._deploy_book.deploy_flows) == 1
        assert deploybook._deploy_book.deploy_flows[0].interval is None
        assert deploybook._deploy_book.deploy_flows[0].cron == "0 0 * * *"


def test_register_should_register_many_flow_for_deployments():
    # Arrange
    with deploybook.use_dedicated_deploybook():
        @deploybook.register(interval=90, name="hello2")
        @deploybook.register(interval=60)
        @flow()
        def myflow3() -> int:
            return 43

        assert len(deploybook._deploy_book.deploy_flows) == 2
        assert deploybook._deploy_book.deploy_flows[0].interval == 60
        assert deploybook._deploy_book.deploy_flows[1].interval == 90
        assert deploybook._deploy_book.deploy_flows[1].name == "hello2"


def test_register_should_refuse_cron_and_interval_for_deployments():
    # Arrange
    with deploybook.use_dedicated_deploybook():
        try:
            @deploybook.register(interval=90, cron="*/3 * * * *")
            @flow()
            def myflow4() -> int:
                return 43

        except ValueError as e:
            assert "Cannot define both interval and cron for the flow" in str(e)
