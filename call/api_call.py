from logs.log_filter import retrieved_Jctl_log
import requests

# Function to send logs to the FastAPI analyzer endpoint
def send_to_api_analyzer(log_ft):
    url = "http://192.168.1.105:8000/analyzer"
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

# Main function to run the script
def main():
    # Define filters for logs
    time = "15 days ago"
    severity = "warning"
    # Retrieve filtered logs
    logs_ft = retrieved_Jctl_log(time, severity)
    # Send logs to the API for analysis
    response_ia = send_to_api_analyzer(logs_ft)
    response_ia_json = response_ia.json()
    print(response_ia.status_code)
    print(response_ia_json)

# This block runs only if the script is executed directly
if __name__ == "__main__":
    main()
