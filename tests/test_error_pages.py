def test__404_page_loads__succeeds(client):
    """Make sure 404 page loads when non existent page is requested"""
    response = client.get('/non_existent_page')
    assert response.status == '404 NOT FOUND'
    assert b'Page Not Found' in response.data
