from pathlib import Path

from tests.python.conftest import GlobalConftest


class TestRoundRobinBalancer:

    async def test_success(self, tmp_path: Path) -> None:
        async with GlobalConftest.running_server(tmp_path):
            responses = [await GlobalConftest.send_request() for _ in range(4)]

            assert "X-Upstream: 9001" in responses[0]
            assert "X-Upstream: 9002" in responses[1]
            assert "X-Upstream: 9001" in responses[2]
            assert "X-Upstream: 9002" in responses[3]
