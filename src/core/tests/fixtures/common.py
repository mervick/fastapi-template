import asyncio
from collections.abc import Generator

import pytest


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest) -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        yield loop
    finally:
        loop.close()
