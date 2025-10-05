from pathlib import Path

from tests.python.conftest import GlobalConftest


class TestProxyRequesting:
    # todo: реализовать переключение на другой upstream, в случае ошибки текущего

    async def test_success(self, tmp_path: Path) -> None:
        async with GlobalConftest.running_server(tmp_path):
            response = await GlobalConftest.send_request()
            assert "200 OK" in response
            assert "X-Upstream: 9001" in response
