from app.alerts.state_store import AlertStateStore


def test_state_store_initializes_missing_file(tmp_path):
    store = AlertStateStore(str(tmp_path / "alert_state.json"))

    state = store.load()

    assert state["active_alerts"] == {}
    assert state["last_sent_at"] is None


def test_state_store_handles_corrupt_file(tmp_path):
    state_file = tmp_path / "alert_state.json"
    state_file.write_text("not-json", encoding="utf-8")
    store = AlertStateStore(str(state_file))

    state = store.load()

    assert state["active_alerts"] == {}
    assert "state_error" in state
