from client.api_call import send_log_to_api_analyzer
from client.api_call import send_mail_to_api

# Test the send_to_api_analyzer function with a mocked API response
def test_send_log_to_api_analyer(mocker):
    # Create a fake response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"llm_resp": "ok"}
    # Mock the requests.post call to return the fake response
    mocker.patch("client.api_call.requests.post", return_value=mock_response)
    
    # Call the function
    response = send_log_to_api_analyzer("test_log")
    
    # Check that the response status code is correct
    assert response.status_code == 200
    # Check that the JSON response is correct
    assert response.json() == {"llm_resp": "ok"}

# Test the send_mail_to_api function with a mocked API response
def test_send_mail_to_api(mocker):
    # Create a fake response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Email send"}
    # Mock the requests.post call to return the fake response
    mocker.patch("client.api_call.requests.post", return_value=mock_response)

    # Call the function
    response = send_mail_to_api("test_content")

    # Check that the response status code is correct
    assert response.status_code == 200
    # Check that the JSON response is correct
    assert response.json.return_value == {"Email send"}