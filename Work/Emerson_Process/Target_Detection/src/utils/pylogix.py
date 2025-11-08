from __future__ import annotations

import threading
import queue
import time
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    from pylogix import PLC
except Exception as e:
    PLC = None
    _import_error = e
else:
    _import_error = None


@dataclass
class PLCConfig:
    ip: str = "192.168.1.6"
    slot: int = 0
    target1_tag: str = "Target1_Hit"
    target2_tag: str = "Target2_Hit"
    reconnect_interval_s: float = 2.0
    write_retry_interval_s: float = 0.25


class PLCWriter:
    def __init__(self, config: PLCConfig):
        if PLC is None:
            raise ImportError(
                f"pylogix library is not available: {_import_error}"
            )
        self.config = config
        self._comm: Optional[PLC] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._q: "queue.Queue[Tuple[bool, bool]]" = queue.Queue(maxsize=1)
        self._last_written: Optional[Tuple[bool, bool]] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self, join_timeout: float = 1.0) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=join_timeout)
        self._disconnect()

    def update_targets(self, target1_hit: bool, target2_hit: bool) -> None:
        state = (bool(target1_hit), bool(target2_hit))
        try:
            self._q.put_nowait(state)
        except queue.Full:
            try:
                _ = self._q.get_nowait()
            except Exception:
                pass
            try:
                self._q.put_nowait(state)
            except Exception:
                pass

    def _connect(self) -> bool:
        try:
            if self._comm is None:
                self._comm = PLC()
            self._comm.IPAddress = self.config.ip
            self._comm.ProcessorSlot = self.config.slot
            return True
        except Exception:
            self._disconnect()
            return False

    def _disconnect(self) -> None:
        try:
            if self._comm is not None:
                try:
                    self._comm.Close()
                except Exception:
                    pass
        finally:
            self._comm = None

    def _ensure_connected(self) -> bool:
        if self._comm is None:
            return self._connect()
        return True

    def _write_tag(self, tag: str, value: bool) -> bool:
        try:
            if not self._ensure_connected():
                return False
            res = self._comm.Write(tag, bool(value))
            if isinstance(res, list):
                ok = all(getattr(r, "Status", "") == "Success" for r in res)
            else:
                ok = getattr(res, "Status", "") == "Success"
            if not ok:
                return False
            return True
        except Exception:
            self._disconnect()
            return False

    def _write_states(self, desired: Tuple[bool, bool]) -> None:
        # Only write on change to avoid spamming
        if self._last_written is None or self._last_written[0] != desired[0]:
            if not self._write_tag(self.config.target1_tag, desired[0]):
                # Failed write; retry later
                return
        if self._last_written is None or self._last_written[1] != desired[1]:
            if not self._write_tag(self.config.target2_tag, desired[1]):
                # Failed write; retry later
                return
        self._last_written = desired

    def _run(self) -> None:
        # Attempt initial connect
        next_reconnect = 0.0
        while not self._stop.is_set():
            try:
                try:
                    desired = self._q.get(timeout=0.1)
                except queue.Empty:
                    continue

                # Coalesce multiple queued updates; keep only the latest
                while True:
                    try:
                        desired = self._q.get_nowait()
                    except queue.Empty:
                        break

                # If not connected, throttle reconnection attempts
                now = time.monotonic()
                if self._comm is None and now < next_reconnect:
                    time.sleep(min(0.05, next_reconnect - now))
                    continue

                if self._comm is None:
                    if not self._connect():
                        next_reconnect = time.monotonic() + self.config.reconnect_interval_s
                        continue

                self._write_states(desired)
            except Exception:
                time.sleep(self.config.write_retry_interval_s)


# Convenience singleton for simple usage from main
_default_writer: Optional[PLCWriter] = None


def init_default(config: Optional[PLCConfig] = None) -> PLCWriter:
    global _default_writer
    if config is None:
        config = PLCConfig()
    if _default_writer is None:
        _default_writer = PLCWriter(config)
        _default_writer.start()
    return _default_writer


def update_default(target1_hit: bool, target2_hit: bool) -> None:
    if _default_writer is None:
        init_default()
    _default_writer.update_targets(
        target1_hit, target2_hit)  # type: ignore[union-attr]


def shutdown_default() -> None:
    global _default_writer
    if _default_writer is not None:
        _default_writer.stop()
        _default_writer = None
