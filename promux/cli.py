import json
import os
import sys
from pathlib import Path

CONFIG_PATH = Path(os.getenv("APPDATA")) / "promux" / "config.json"


def save_config(projects_dir):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps({"projects_dir": str(projects_dir)}, indent=2),
        encoding="utf-8",
    )


def load_config():
    if not CONFIG_PATH.exists():
        print("Promux is not configured.", file=sys.stderr)
        print("Run: py -m promux.cli init C:\\path\\to\\projects", file=sys.stderr)
        raise SystemExit(1)

    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def init(path):
    projects_dir = Path(path).resolve()

    if not projects_dir.exists() or not projects_dir.is_dir():
        print(f"Invalid directory: {projects_dir}")
        raise SystemExit(1)

    save_config(projects_dir)
    print(f"Promux directory set to: {projects_dir}")


def get_projects():
    config = load_config()
    root = Path(config["projects_dir"])

    return sorted(
        [p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")],
        key=lambda p: p.name.lower(),
    )


def list_projects():
    for project in get_projects():
        print(project.name)


def switch():
    projects = get_projects()

    if not projects:
        print("No projects found.", file=sys.stderr)
        raise SystemExit(1)

    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project.name}", file=sys.stderr)

    print("Choose project: ", end="", file=sys.stderr, flush=True)
    choice = sys.stdin.readline().strip()

    if not choice.isdigit():
        raise SystemExit(1)

    index = int(choice) - 1

    if index < 0 or index >= len(projects):
        raise SystemExit(1)

    print(projects[index])


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  py -m promux.cli init C:\\path\\to\\projects")
        print("  py -m promux.cli list")
        print("  py -m promux.cli switch")
        return

    command = args[0]

    if command == "init":
        if len(args) < 2:
            print("Missing projects directory.")
            raise SystemExit(1)

        init(args[1])
        return

    if command == "list":
        list_projects()
        return

    if command == "switch":
        switch()
        return

    print(f"Unknown command: {command}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
