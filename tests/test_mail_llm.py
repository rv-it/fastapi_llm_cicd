from mail.mail_llm import send_email
from smtplib import SMTPAuthenticationError, SMTPException
from fastapi import HTTPException
import pytest

# Test the send_email function success
def test_send_email(mocker):
    # mock the connexion to the smtp server 
    # no return_value because it brokes the context manager "with" ('str' object does not support the context manager protocol)
    mock_smtp = mocker.patch("mail.mail_llm.smtplib.SMTP")
    # run the function send_email
    result = send_email("llm_response", "smtp_srv", 587, "bob@mail.com", "dylan@mail.com")

    # Verify that send_email was called with the correct argument
    mock_smtp.assert_called_once_with("smtp_srv", 587)
    # Check that the result content is correct
    assert "Email send to" in result

# These tests verify that send_email correctly handles exceptions from the LLM and converts them into HTTPException
# Test authentication error handling
def test_auth_error(mocker):
    # Mock the connexion to the smtp server to raise an AuthenticationError
    mocker.patch("mail.mail_llm.smtplib.SMTP", side_effect=SMTPAuthenticationError(msg="cred invalid", code=401))
    
    # Expect an HTTPException when calling send_emaiil
    with pytest.raises(HTTPException) as exc:
        # run the function send_email
        send_email("llm_response", "smtp_srv", 587, "bob@mail.com", "dylan@mail.com")
    # Check status code and error message
    assert exc.value.status_code == 401
    assert "cred invalid" in exc.value.detail

# Test SMTP error handling
def test_generic_smtp_error(mocker):
    # Mock the connexion to the smtp server to raise a SMTPException
    mocker.patch("mail.mail_llm.smtplib.SMTP", side_effect=SMTPException("smtp error"))

    with pytest.raises(HTTPException) as exc:
        send_email("llm_response", "smtp_srv", 587, "bob@mail.com", "dylan@mail.com")

    assert exc.value.status_code == 500
    assert "smtp error" in exc.value.detail

# Test unexpected exception handling
def test_other_error(mocker):
    # Mock the connexion to the smtp server to raise a SMTPException
    mocker.patch("mail.mail_llm.smtplib.SMTP", side_effect=Exception("Unexpected error"))

    with pytest.raises(HTTPException) as exc:
        send_email("llm_response", "smtp_srv", 587, "bob@mail.com", "dylan@mail.com")

    assert exc.value.status_code == 500
    assert exc.value.detail == "Unexpected error"