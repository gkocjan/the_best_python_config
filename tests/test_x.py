def test_x(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")

    assert False
