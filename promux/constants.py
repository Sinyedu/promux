from pathlib import Path

APP_NAME = "promux"

CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_EDITOR = "nvim"
