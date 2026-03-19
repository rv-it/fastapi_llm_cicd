from client.log_filter import retrieved_Jctl_log

# Test the retrieved_Jctl_log function with mocked journalctl output
def test_retrieved_Jctl_log(mocker):
    # Create a fake subprocess result with sample logs
    mock_log = mocker.Mock()
    mock_log.stdout = """Nov 11 10:38:22 srv_lenny kernel: disaster in progress
    Nov 12 08:37:50 srv_lenny systemd[1]: This isn't very good at all
    Nov 12 08:40:50 srv_lenny systemd[1]: This isn't very good at all
    Nov 12 08:42:50 srv_lenny systemd[1]: This isn't very good at all"""

    # Mock subprocess.run to return the fake logs
    mocker.patch("client.log_filter.subprocess.run", return_value=mock_log)

    # Call the function
    log_dic = retrieved_Jctl_log("", "")
     # Check that the result is a dictionary
    assert isinstance(log_dic, dict)
    # Check that identical logs are grouped (2 unique messages expected)
    assert len(log_dic) == 2
    # Check that keys follow the expected format: "log X"
    for key in log_dic.keys():
        assert key.startswith("log ")


