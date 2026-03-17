from fastapi.testclient import TestClient
from main import app

# Create a test client for the FastAPI app
client = TestClient(app)

# Test the /analyzer endpoint
def test_analyzer_endpoint(mocker):
    # Mock the analyze_log function to avoid calling the real LLM
    mock_analyze = mocker.patch(
        "main.analyze_log",
        return_value={"analysis": "ok"}
    )
    # Send a POST request to the endpoint with test data
    response = client.post(
        "/analyzer",
        json={"text": "error log"}
    )
    # Check that the request was successful
    assert response.status_code == 200
    # Check that the response content is correct
    assert response.json() == {"analysis": "ok"}
    # Verify that analyze_log was called with the correct argument
    mock_analyze.assert_called_once_with("error log")