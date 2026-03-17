import subprocess
from collections import Counter

# Function to retrieve and format journalctl logs
def retrieved_Jctl_log(time: str, severity: str):
    # Run the journalctl command and capture the output
    logs = subprocess.run(["journalctl", "--since", time,"-p", severity], capture_output=True, text=True)
    # Places each log lines into an array
    lines = logs.stdout.splitlines()

    messages = []
    # Extract only the message part of each log line (remove the first elements like date, host, service, etc.)
    for line in lines:
        message = " ".join(line.split()[4:])
        messages.append(message)
     # Group identical messages and count occurrences
    counts = Counter(messages)
    
    
    # Format logs to send to the LLM
    log_dic = {}
    i = 1
    for msg, count in counts.items():
        log_dic[f"log {i}"] = f"{count}x -> {msg} \n"
        i += 1
    
    return log_dic

  
