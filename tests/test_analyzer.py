from ai.analyzer import analyze_log
from litellm import AuthenticationError, RateLimitError, APIError 
from fastapi import HTTPException
import pytest
import os

# Test the analyze_log function success
def test_analyze_log(mocker):
    # simulates api key
    mocker.patch("ai.analyzer.os.getenv", return_value="fake_api_key")
    # Create a fake completion result with fake content ("ok")
    mock_response = mocker.Mock()
    mock_response.choices = [
        mocker.Mock(message=mocker.Mock(content="ok"))
    ]
    # mock the call to the LLM
    mock_llm = mocker.patch("ai.analyzer.completion", return_value=mock_response)
    # run the analyze_log function
    result = analyze_log("test_log", "model")
    # Check that the response content is correct
    assert result == "ok"
    mock_llm.assert_called_once()

# These tests verify that analyze_log correctly handles exceptions from the LLM and converts them into HTTPException
# Test authentication error handling
def test_auth_err(mocker):
    # simulates api key
    mocker.patch("ai.analyzer.os.getenv", return_value="fake_api_key")
    # Mock the LLM call to raise an AuthenticationError
    mocker.patch("ai.analyzer.completion", side_effect=AuthenticationError(message="Key invalid", llm_provider="llm", model="model"))
    
    # Expect an HTTPException when calling analyze_log
    with pytest.raises(HTTPException) as exc:
        # run the fonction analyze log
        analyze_log("test_log", "model")
    # Check status code and error message
    assert exc.value.status_code == 401
    assert f"Key invalid" in str(exc.value.detail)

# Test rate limit error handling
def test_rate_err(mocker):
    # simulates api key
    mocker.patch("ai.analyzer.os.getenv", return_value="fake_api_key")    
    # Mock the LLM call to raise an RateLimitError
    mocker.patch("ai.analyzer.completion", side_effect=RateLimitError(message="Limit reached", llm_provider="llm", model="model"))
       
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log", "model")

    assert exc.value.status_code == 429
    assert f"Limit reached" in str(exc.value.detail)

# Test generic API error handling
def test_api_err(mocker):
    # simulates api key
    mocker.patch("ai.analyzer.os.getenv", return_value="fake_api_key")
    # Mock the LLM call to raise an APIError
    mocker.patch("ai.analyzer.completion", side_effect=APIError(message="Api error", status_code="500", llm_provider="llm", model="model"))
     
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log", "model")

    assert exc.value.status_code == 500
    assert f"Api error" in str(exc.value.detail)

# Test unexpected exception handling
def test_other_err(mocker):
    # simulates api key
    mocker.patch("ai.analyzer.os.getenv", return_value="fake_api_key")
    # Mock the LLM call to raise unknown exception
    mocker.patch("ai.analyzer.completion", side_effect=Exception("Unexpected error"))
  
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log", "model")

    assert exc.value.status_code == 500
    assert f"Unexpected error" in str(exc.value.detail)