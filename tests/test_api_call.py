from client.api_call import send_to_api_analyzer

# Test the send_to_api_analyzer function with a mocked API response
def test_send_to_api_analyer(mocker):
    # Create a fake response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"llm_resp": "ok"}
    # Mock the requests.post call to return the fake response
    mocker.patch("client.api_call.requests.post", return_value=mock_response)
    
    # Call the function
    response = send_to_api_analyzer("test_log")
    
    # Check that the response status code is correct
    assert response.status_code == 200
    # Check that the JSON response is correct
    assert response.json() == {"llm_resp": "ok"}