from watchfiles import run_process, Change

from core import start_server, settings


def py_filter(change: Change, path: str) -> bool:
    return path.endswith(".py")


if __name__ == "__main__":
    if settings.DEPLOY:
        mode = "DEPLOYMENT MODE"
        start_server(mode)
    else:
        mode = "DEVELOPMENT MODE"
        run_process(
            "./",
            target=start_server,
            args=(mode,),
            watch_filter=py_filter,
        )
