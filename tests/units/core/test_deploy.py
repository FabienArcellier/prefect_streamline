from prefect_streamline.core.deploy import DeployFlow


def test_format_on_deploybook_should_format_a_readable_name():
    # Arrange
    def fake_flow():
        pass

    deploy = DeployFlow(fake_flow, interval=60)
    # Act
    # Assert
    assert "fake_flow (name:main, interval:60)" == deploy.format()
