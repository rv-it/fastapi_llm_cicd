from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_analyzer_endpoint(mocker):

    mock_analyze = mocker.patch(
        "main.analyze_log",
        return_value={"analysis": "ok"}
    )

    response = client.post(
        "/analyzer",
        json={"text": "error log"}
    )

    assert response.status_code == 200
    assert response.json() == {"analysis": "ok"}
    mock_analyze.assert_called_once_with("error log")