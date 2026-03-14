from call.api_call import send_to_api_analyer

def test_send_to_api_analyer(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"llm_resp": "ok"}
    
    mocker.patch("call.api_call.requests.post", return_value=mock_response)

    response = send_to_api_analyer("test_log")

    assert response.status_code == 200
    assert response.json() == {"llm_resp": "ok"}