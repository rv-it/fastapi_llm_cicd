from client.log_filter import retrieved_Jctl_log
import requests

api_hots_ip = "192.168.1.105"

# Function to send logs to the FastAPI analyzer endpoint
def send_log_to_api_analyzer(log_ft):
    url = f"http://{api_hots_ip}:8000/analyzer"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": f"{log_ft}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        # Raise HTTPError exception
        response.raise_for_status()
        return response
    # Capture all exception
    except requests.RequestException as e:
        # display exception message
        print(e)
        # return the full response of the API
        return response
    
def send_mail_to_api(llm_response):
    url = f"http://{api_hots_ip}:8000/mail"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "content": llm_response,
        "smtp_srv": "smtp.gmail.com",
        "port": 587,
        "receiver": "chrom_1@hotmail.fr"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(e)
        return response

# Main function to run the script
def main():
    # Define filters for logs
    time = "15 days ago"
    severity = "warning"
    # Retrieve filtered logs
    logs_ft = retrieved_Jctl_log(time, severity)
    # Send logs to the API for analysis
    response_ia = send_log_to_api_analyzer(logs_ft)
    response_ia_json = response_ia.json()
    mail = send_mail_to_api(response_ia_json)
    print(mail)

# This block runs only if the script is executed directly
if __name__ == "__main__":
    main()
