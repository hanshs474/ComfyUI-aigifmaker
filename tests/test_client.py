import importlib.util
import os
import sys

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("aigifmaker_client", os.path.join(HERE, "aigifmaker_client.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)


def seq(*bodies):
    it = iter(bodies)
    return lambda method, url, body, headers: (200, next(it))


def test_generate_queue_then_success():
    t = seq(
        {"code": 0, "data": {"id": "t1", "status": "pending"}},
        {"code": 0, "data": {"id": "t1", "status": "processing", "queued": True}},
        {"code": 0, "data": {"id": "t1", "status": "success", "images": ["https://x/a.gif"]}},
    )
    assert gm.Client("sk", transport=t, poll_every=0).generate("a corgi") == "https://x/a.gif"


@pytest.mark.parametrize("body,err", [
    ({"code": -1, "message": "invalid API key"}, gm.AuthError),
    ({"code": 0, "data": {"wall": True}}, gm.AuthError),
    ({"code": -1, "message": "insufficient credits"}, gm.QuotaError),
    ({"code": 429, "message": "cooldown"}, gm.RejectedError),
])
def test_errors(body, err):
    with pytest.raises(err):
        gm.Client("sk", transport=seq(body)).submit("x")


def test_failed():
    t = seq({"code": 0, "data": {"id": "t1"}}, {"code": 0, "data": {"status": "failed", "errorMessage": "boom"}})
    with pytest.raises(gm.GenerationFailed):
        gm.Client("sk", transport=t, poll_every=0).generate("x")




# live smoke, free (no generation)
def test_live_wrong_key():
    with pytest.raises(gm.AuthError):
        gm.Client("sk-invalidtest000").credits()


def test_live_no_key(monkeypatch):
    monkeypatch.delenv("AIGIFMAKER_API_KEY", raising=False)
    with pytest.raises(gm.AuthError):
        gm.Client().submit("smoke test")
