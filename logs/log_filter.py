import subprocess
from collections import Counter


def retrieved_Jctl_log(time: str, severity: str):
    logs = subprocess.run(["journalctl", "--since", time,"-p", severity], capture_output=True, text=True)

    lines = logs.stdout.splitlines()

    messages = []
    for line in lines:
        message = " ".join(line.split()[4:])
        messages.append(message)

    counts = Counter(messages)

    log_dic = {}
    i = 1
    for msg, count in counts.items():
        log_dic[f"log {i}"] = f"{count}x -> {msg} \n"
        i += 1
    
    return log_dic

  
