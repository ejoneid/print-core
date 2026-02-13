import asyncio
import threading
from typing import Optional

import asyncssh

from print_core.config import get_settings


class ReverseSSHTunnel:
    def __init__(
        self,
        host: str,
        username: str,
        password: Optional[str],
        remote_bind_host: str,
        remote_bind_port: int,
        local_bind_host: str,
        local_bind_port: int,
    ) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._remote_bind_host = remote_bind_host
        self._remote_bind_port = remote_bind_port
        self._local_bind_host = local_bind_host
        self._local_bind_port = local_bind_port

        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._started = threading.Event()
        self._stop_event: Optional[asyncio.Event] = None
        self._conn: Optional[asyncssh.SSHClientConnection] = None
        self._forwarder: Optional[asyncssh.SSHListener] = None

    async def _run(self) -> None:
        self._stop_event = asyncio.Event()
        async with asyncssh.connect(
            self._host,
            username=self._username,
            password=self._password,
        ) as conn:
            self._conn = conn
            self._forwarder = await conn.forward_remote_port(
                self._remote_bind_host,
                self._remote_bind_port,
                self._local_bind_host,
                self._local_bind_port,
            )
            self._started.set()
            await self._stop_event.wait()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def _runner() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._run())
            finally:
                pending = asyncio.all_tasks(self._loop)
                for task in pending:
                    task.cancel()
                self._loop.run_until_complete(self._loop.shutdown_asyncgens())
                self._loop.close()

        self._thread = threading.Thread(
            target=_runner, name="reverse-ssh-tunnel", daemon=True
        )
        self._thread.start()
        self._started.wait(timeout=10)

    def stop(self) -> None:
        if not self._loop or not self._stop_event:
            return

        def _shutdown() -> None:
            if self._forwarder is not None:
                self._forwarder.close()
            if self._conn is not None:
                self._conn.close()
            if self._stop_event is not None:
                self._stop_event.set()

        self._loop.call_soon_threadsafe(_shutdown)
        if self._thread:
            self._thread.join(timeout=10)


settings = get_settings()
tunnel = ReverseSSHTunnel(
    host=settings.print_flow_host,
    username=settings.print_flow_host_user,
    password=settings.print_flow_host_password,
    remote_bind_host="127.0.0.1",
    remote_bind_port=18000,
    local_bind_host="127.0.0.1",
    local_bind_port=8000,
)
