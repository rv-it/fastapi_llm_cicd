from log.log_filter import retrieved_Jctl_log, send_to_api_analyer

def test_retrieved_Jctl_log():
    result = retrieved_Jctl_log("6 hours ago", "info")
    assert isinstance(result, dict)
    for key in result.keys():
        assert key.startswith("log")


def test_send_to_api_analyer():
    response = send_to_api_analyer("test")    
    assert response is not None
    assert response.json() is not None
    assert response.status_code == 200



    

