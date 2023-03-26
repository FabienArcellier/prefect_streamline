from prefect import flow

from prefect_streamline import deploybook


@deploybook.register(interval=90, name="hello2")
@deploybook.register(interval=60)
@flow()
def myflow3() -> int:
    return 43
