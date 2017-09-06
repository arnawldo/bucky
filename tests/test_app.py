def test__hello_world__succeeds(client):
    """test hello world from basic app"""
    r = client.get('/')
    assert b"Hello" in r.data
