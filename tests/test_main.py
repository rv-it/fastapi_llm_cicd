from fastapi.testclient import TestClient
from main import app

# Create a test client for the FastAPI app
client = TestClient(app)

# Test the /analyzer endpoint
def test_analyzer_endpoint(mocker):
    payload = {
        "text": "error log",
        "model": "model"
    }
    # Mock the analyze_log function to avoid calling the real LLM
    mock_analyze = mocker.patch("main.analyze_log", return_value={"analysis": "ok"})
    # Send a POST request to the endpoint with test payload
    response = client.post("/analyzer", json=payload)
    # Check that the request was successful
    assert response.status_code == 200
    # Check that the response content is correct
    assert response.json() == {"analysis": "ok"}
    # Verify that analyze_log was called with the correct argument
    mock_analyze.assert_called_once_with("error log", "model")

# Test the /mail endpoint
def test_mail_endpoint(mocker):
    payload = {
        "content": "llm_response",
        "smtp_srv": "smtp_srv",
        "port": 587,
        "sender": "bob@mail.com",
        "receiver": "dylan@mail.com"
    }
    # Mock the send_email function to avoid sending real mail
    mock_mail = mocker.patch("main.send_email", return_value=("Email send"))
    # Send a POST request to the endpoint with test payload
    response = client.post("/mail",json=payload)
    # Check that the request was successful
    assert response.status_code == 200
    # Check that the response content is correct
    assert response.json() == ("Email send")
    # Verify that send_email was called with the correct argument
    mock_mail.assert_called_once_with("llm_response", "smtp_srv", 587, "bob@mail.com", "dylan@mail.com")

