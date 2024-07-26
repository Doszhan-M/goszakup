from watchfiles import run_process, Change

from core import start_server


def py_filter(change: Change, path: str) -> bool:
    return path.endswith(".py") and "signer" in path


if __name__ == "__main__":
    mode = "HOT RELOAD MODE"
    run_process(
        "./",
        target=start_server,
        args=(mode,),
        watch_filter=py_filter,
    )
