"""Configuration management: load settings from config/config.json."""
import json
import os

# Project root = two levels above src/utils/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_CONFIG = {
    "data_file": "data/students.json",
    "export_file": "data/students_export.csv",
    "log_file": "logs/app.log",
    "log_level": "INFO",
}


def load_config(path: str = None) -> dict:
    """Load config, falling back to defaults. Env var SIS_CONFIG overrides the path.

    Relative file paths are resolved against the project root so the app
    works no matter which directory it is launched from (cloud-friendly).
    """
    path = path or os.environ.get("SIS_CONFIG") or os.path.join(ROOT_DIR, "config", "config.json")
    config = dict(DEFAULT_CONFIG)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            config.update(json.load(fh))
    except FileNotFoundError:
        print(f"Config file not found at {path}; using defaults.")
    except json.JSONDecodeError as exc:
        print(f"Config file is invalid ({exc}); using defaults.")

    for key in ("data_file", "export_file", "log_file"):
        if not os.path.isabs(config[key]):
            config[key] = os.path.join(ROOT_DIR, config[key])
    return config
