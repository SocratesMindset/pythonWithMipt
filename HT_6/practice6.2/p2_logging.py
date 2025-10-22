from datetime import datetime
from typing import Any, Callable

class LogManager:
    def __init__(self, path: str = "Log.txt", user: str | None = None, session: str | None = None):
        self.path = path
        self.user = user
        self.session = session
        self._f = None

    def __enter__(self):
        self._f = open(self.path, "a", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._f:
            self._f.close()
        return False

    def log(self, level: str, source: str, message: str, event_id: str | None = None, extra: Any | None = None):
        ts = datetime.now().isoformat(sep=" ", timespec="seconds")
        eid = event_id if event_id is not None else "-"
        usr = self.user if self.user is not None else "-"
        ses = self.session if self.session is not None else "-"
        add = "" if extra is None else str(extra)
        line = f"{ts} | {level.upper()} | {source} | {message} | id={eid} | user={usr} | session={ses} | {add}\n"
        if self._f is None:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line)
        else:
            self._f.write(line)

def safe_call(fn: Callable, *args, log: LogManager, level_ok: str = "INFO", level_err: str = "ERROR",
              source: str = "app", event_id: str | None = None, extra_ok: Any | None = None,
              extra_err: Any | None = None, **kwargs):
    try:
        res = fn(*args, **kwargs)
        log.log(level_ok, source, f"ok: {fn.__name__}", event_id=event_id, extra=extra_ok)
        return res
    except FileNotFoundError as e:
        log.log(level_err, source, f"file_error: {fn.__name__}: {e}", event_id=event_id, extra=extra_err)
        raise
    except IsADirectoryError as e:
        log.log(level_err, source, f"dir_error: {fn.__name__}: {e}", event_id=event_id, extra=extra_err)
        raise
    except ValueError as e:
        log.log(level_err, source, f"value_error: {fn.__name__}: {e}", event_id=event_id, extra=extra_err)
        raise
    except OSError as e:
        log.log(level_err, source, f"os_error: {fn.__name__}: {e}", event_id=event_id, extra=extra_err)
        raise
    except Exception as e:
        log.log("FATAL", source, f"unexpected: {fn.__name__}: {e}", event_id=event_id, extra=extra_err)
        raise
