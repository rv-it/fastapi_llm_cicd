import subprocess
from collections import Counter
import requests


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

def send_to_api_analyer(log_ft):
    url = "http://127.0.0.1:8000/analyzer"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": f"{log_ft}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        # e ne renvoi que par exemple 401 Client Error: Unauthorized for url: http://127.0.0.1:8000/analyzer pour detail il faut return response
        print(e)
        # si pas "return response" si exception main() a rien dans reponse (response_ia = None) -> response_ia_json = response_ia.json()v AttributeError: 'NoneType' object has no attribute 'json'
        # permet aussi de voir les erreur gérer par litellm (ex: litellm.AuthenticationError) car c'est la réponse que reçoit notre API en cas de problème
        return response

def main():
    time = "15 days ago"
    severity = "warning"
    logs_ft = retrieved_Jctl_log(time, severity)
    response_ia = send_to_api_analyer(logs_ft)
    response_ia_json = response_ia.json()
    print(response_ia.status_code)
    print(response_ia_json)

if __name__ == "__main__":
    main()

  
