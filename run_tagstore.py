"""Desktop launcher for TagStore.

Picks an image folder, starts the local server on a free localhost port, and
opens it in a native window. PyInstaller builds this file. Developers can run::

    python run_tagstore.py
    python run_tagstore.py --root C:\\path\\to\\images

``python -m tagstore.web --root <folder>`` still starts the server without a window.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from logging.handlers import RotatingFileHandler

APP_NAME = "TagStore"
HOST = "127.0.0.1"


def app_data_dir():
    base = os.environ.get("APPDATA")
    if not base:
        base = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def config_path():
    return os.path.join(app_data_dir(), "config.json")


def log_path():
    return os.path.join(app_data_dir(), "tagstore.log")


def setup_logging():
    """Log to %APPDATA%\\TagStore\\tagstore.log.

    A windowed PyInstaller build has no console, and uvicorn's default log
    config crashes when sys.stderr is None. The server is started with
    log_config=None so these handlers are the only ones.
    """
    handler = RotatingFileHandler(log_path(), maxBytes=1_000_000, backupCount=1, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    if sys.stderr is not None:
        stream = logging.StreamHandler()
        stream.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        root.addHandler(stream)


def load_last_root():
    try:
        with open(config_path(), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    root = data.get("last_root") if isinstance(data, dict) else None
    if isinstance(root, str) and os.path.isdir(root):
        return os.path.abspath(root)
    return None


def save_last_root(root):
    with open(config_path(), "w", encoding="utf-8") as f:
        json.dump({"last_root": os.path.abspath(root)}, f, indent=2)
        f.write("\n")


def choose_folder():
    """Ask for an image folder. Returns None when the user cancels or the dialog cannot open."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        logging.exception("folder dialog is unavailable")
        return None

    ui = tk.Tk()
    ui.withdraw()
    try:
        ui.attributes("-topmost", True)
    except tk.TclError:
        pass
    try:
        path = filedialog.askdirectory(title="Choose the folder that contains your images")
    finally:
        ui.destroy()
    if not path:
        return None
    return os.path.abspath(path)


def resolve_root(cli_root):
    if cli_root:
        root = os.path.abspath(cli_root)
        if not os.path.isdir(root):
            logging.error("not a folder: %s", root)
            raise SystemExit(1)
        return root
    saved = load_last_root()
    if saved:
        return saved
    chosen = choose_folder()
    if not chosen:
        logging.info("folder selection cancelled")
        raise SystemExit(0)
    return chosen


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def start_server(root, port):
    import uvicorn

    from tagstore.web import create_app

    app = create_app(root)
    config = uvicorn.Config(
        app,
        host=HOST,
        port=port,
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, name="tagstore-server", daemon=True)
    thread.start()
    return server, thread


def wait_until_up(port, timeout=20.0):
    url = f"http://{HOST}:{port}/"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.5) as resp:
                if resp.status < 500:
                    return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(0.1)
    return False


def open_window(url):
    import webview

    webview.create_window(APP_NAME, url, width=1200, height=800)
    webview.start(gui="edgechromium")


def open_browser_fallback(url):
    logging.warning(
        "Could not open a native window. TagStore is at %s. "
        "End TagStore from Task Manager to stop it.",
        url,
    )
    webbrowser.open(url)
    threading.Event().wait()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run TagStore in a desktop window.")
    parser.add_argument("--root", help="Image folder. Remembered for the next launch.")
    args = parser.parse_args(argv)

    setup_logging()
    try:
        root = resolve_root(args.root)
        save_last_root(root)
        port = free_port()
        logging.info("starting TagStore root=%s port=%s", root, port)
        _server, _thread = start_server(root, port)
        if not wait_until_up(port):
            logging.error("server did not start on %s:%s", HOST, port)
            return 1
        url = f"http://{HOST}:{port}/"
        try:
            open_window(url)
        except Exception:
            logging.exception("native window failed")
            open_browser_fallback(url)
        return 0
    except SystemExit as exc:
        code = exc.code
        if isinstance(code, int):
            return code
        return 1 if code else 0
    except Exception:
        logging.exception("TagStore failed to start")
        return 1


if __name__ == "__main__":
    sys.exit(main())
