from prefect import flow, get_run_logger

from prefect_streamline import flowtest


def test_test_flow_should_execute_the_function_relative_to_a_specific_flow():
    """
    checks that the helper executes the flow that corresponds with the arguments
    """
    assert flowtest.fn(_fake_flow)(12) == 12


def test_test_flow_should_handle_the_logger():
    """
    checks that the helper executes the flow that corresponds with the arguments.
    """
    with flowtest.use_native_runner():
        assert flowtest.fn(_fake_flow_with_logger)() == 12


@flow()
def _fake_flow(arg1: int) -> int:
    return arg1

@flow()
def _fake_flow_with_logger() -> int:
    logger = get_run_logger()
    return 12
