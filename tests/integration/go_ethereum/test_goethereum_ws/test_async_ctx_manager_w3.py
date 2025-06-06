import pytest

import pytest_asyncio

from web3 import (
    AsyncWeb3,
    WebSocketProvider,
)
from web3._utils.module_testing.go_ethereum_admin_module import (
    GoEthereumAsyncAdminModuleTest,
)
from web3._utils.module_testing.persistent_connection_provider import (
    PersistentConnectionProviderTest,
)

from ..common import (
    GoEthereumAsyncDebugModuleTest,
    GoEthereumAsyncEthModuleTest,
    GoEthereumAsyncNetModuleTest,
    GoEthereumAsyncWeb3ModuleTest,
)


@pytest_asyncio.fixture
async def async_w3(start_geth_process_and_yield_port):
    port = start_geth_process_and_yield_port
    # async context manager pattern
    async with AsyncWeb3(
        WebSocketProvider(f"ws://127.0.0.1:{port}", request_timeout=10)
    ) as w3:
        yield w3


class TestGoEthereumAsyncWeb3ModuleTest(GoEthereumAsyncWeb3ModuleTest):
    pass


class TestGoEthereumAsyncAdminModuleTest(GoEthereumAsyncAdminModuleTest):
    @pytest.mark.asyncio
    @pytest.mark.xfail(
        reason="running geth with the --nodiscover flag doesn't allow peer addition"
    )
    async def test_admin_peers(self, async_w3: "AsyncWeb3") -> None:
        await super().test_admin_peers(async_w3)

    @pytest.mark.asyncio
    async def test_admin_start_stop_http(self, async_w3: "AsyncWeb3") -> None:
        # This test causes all tests after it to fail on CI if it's allowed to run
        pytest.xfail(
            reason="Only one HTTP endpoint is allowed to be active at any time"
        )
        await super().test_admin_start_stop_http(async_w3)

    @pytest.mark.asyncio
    async def test_admin_start_stop_ws(self, async_w3: "AsyncWeb3") -> None:
        # This test inconsistently causes all tests after it to
        # fail on CI if it's allowed to run
        pytest.xfail(
            reason="Only one WebSocket endpoint is allowed to be active at any time"
        )
        await super().test_admin_start_stop_ws(async_w3)


class TestPersistentConnectionProviderTest(PersistentConnectionProviderTest):
    pass


class TestGoEthereumAsyncEthModuleTest(GoEthereumAsyncEthModuleTest):
    pass


class TestGoEthereumAsyncNetModuleTest(GoEthereumAsyncNetModuleTest):
    pass


class TestGoEthereumAsyncDebugModuleTest(GoEthereumAsyncDebugModuleTest):
    pass
