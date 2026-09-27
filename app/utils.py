import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("data/history.json")


def _ensure_file():
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")


def load_history():
    _ensure_file()
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_history(result):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "count": result.get("count", 0),
        "summary": result.get("summary", ""),
        "detections": result.get("detections", []),
    })
    HISTORY_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_history():
    HISTORY_FILE.write_text("[]", encoding="utf-8")
