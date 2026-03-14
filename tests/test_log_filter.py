from logs.log_filter import retrieved_Jctl_log

def test_retrieved_Jctl_log(mocker):
    mock_log = mocker.Mock()
    mock_log.stdout = """Nov 11 10:38:22 srv_lenny kernel: disaster in progress
    Nov 12 08:37:50 srv_lenny systemd[1]: This isn't very good at all
    Nov 12 08:40:50 srv_lenny systemd[1]: This isn't very good at all
    Nov 12 08:42:50 srv_lenny systemd[1]: This isn't very good at all"""

    mocker.patch("logs.log_filter.subprocess.run", return_value=mock_log)
    
    log_dic = retrieved_Jctl_log("", "")
    assert isinstance(log_dic, dict)
    assert len(log_dic) == 2
    for key in log_dic.keys():
        assert key.startswith("log ")


