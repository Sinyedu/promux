import json
from pathlib import Path

from promux.constants import CONFIG_DIR, CONFIG_FILE, DEFAULT_EDITOR


def config_exists() -> bool:
    return CONFIG_FILE.exists()


def load_config() -> dict[str, str]:
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config: dict[str, str]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)


def create_config() -> dict[str, str]:
    print("No Promux config found.")
    project_root = input("Where are your projects stored? ")

    config = {
        "projectRoot": str(Path(project_root).expanduser()),
        "editor": DEFAULT_EDITOR,
    }

    save_config(config)

    print(f"Config saved to {CONFIG_FILE}")

    return config


def setup_config() -> dict[str, str]:
    if config_exists():
        config = load_config()
        print(f"Promux config loaded from {CONFIG_FILE}")
        return config

    return create_config()
