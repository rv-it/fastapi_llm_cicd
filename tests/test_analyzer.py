from ai.analyzer import analyze_log
from litellm import AuthenticationError, RateLimitError, APIError 
from fastapi import HTTPException
import pytest


def test_auth_err(mocker):
    mocker.patch("ai.analyzer.completion", side_effect=AuthenticationError(message="Key invalid", llm_provider="llm", model="model"))
    
    # pour capturer mais pas lever l'exception sinon le test échouera
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log")

    assert exc.value.status_code == 401
    assert f"Key invalid" in str(exc.value.detail)

def test_rate_err(mocker):
    mocker.patch("ai.analyzer.completion", side_effect=RateLimitError(message="Limit reached", llm_provider="llm", model="model"))
    
    # pour capturer mais pas lever l'exception sinon le test échouera
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log")

    assert exc.value.status_code == 429
    assert f"Limit reached" in str(exc.value.detail)

def test_api_err(mocker):
    mocker.patch("ai.analyzer.completion", side_effect=APIError(message="Api error", status_code="500", llm_provider="llm", model="model"))
    
    # pour capturer mais pas lever l'exception sinon le test échouera
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log")

    assert exc.value.status_code == 500
    assert f"Api error" in str(exc.value.detail)

def test_other_err(mocker):
    mocker.patch("ai.analyzer.completion", side_effect=Exception("Unexpected error"))
    
    # pour capturer mais pas lever l'exception sinon le test échouera
    with pytest.raises(HTTPException) as exc:
        analyze_log("test_log")

    assert exc.value.status_code == 500
    assert f"Unexpected error" in str(exc.value.detail)