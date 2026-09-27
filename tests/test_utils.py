from app.utils import load_history, save_history, clear_history

def test_history_starts_empty(tmp_path, monkeypatch):
    import app.utils as utils
    utils.HISTORY_FILE = tmp_path / "history.json"

    assert load_history() == []

    save_history({
        "count": 1,
        "summary": "1 objek",
        "detections": [{
            "label": "bottle",
            "category": "Anorganik",
            "confidence": 0.91,
            "recommendation": "Daur ulang"
        }]
    })

    assert len(load_history()) == 1

    clear_history()
    assert load_history() == []
