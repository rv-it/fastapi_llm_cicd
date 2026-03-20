from client.log_filter import retrieved_Jctl_log
import requests
import sys

api_hots_ip = "192.168.1.105"
model = "gemini/gemini-2.5-flash"

# Function to send logs to the FastAPI analyzer endpoint
def send_log_to_api_analyzer(log_ft):
    url = f"http://{api_hots_ip}:8000/analyzer"
    headers = {
        "Content-Type": "application/json"
    }
    # Create the payload with analyzer parameters
    payload = {
        "text": f"{log_ft}",
        "model": model
    }

    try:
        # Send POST request to the API
        response = requests.post(url, headers=headers, json=payload)
        # Raise HTTPError exception if the request failed
        response.raise_for_status()
        return response
    # Capture all exception
    except requests.RequestException as e:
        # display exception message
        print(e)
        # return the full response of the API
        return response
    
# Function to send mail content to the FastAPI mail endpoint    
def send_mail_to_api(llm_response):
    url = f"http://{api_hots_ip}:8000/mail"
    headers = {
        "Content-Type": "application/json"
    }
    # Create the payload with mail parameters
    payload = {
        "content": llm_response,
        "smtp_srv": "smtp.gmail.com",
        "port": 587,
        "sender": "romain.voisin13@gmail.com",
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
    # Define filters for retrieving logs
    time = "25 days ago"
    severity = "warning"
    # Retrieve filtered and formatted logs
    logs_ft = retrieved_Jctl_log(time, severity)
    # Check if there are any logs to process
    if logs_ft == None:
        print("No log to analyze")
        sys.exit(0)
    # Send the filtered logs to the LLM
    response_ia = send_log_to_api_analyzer(logs_ft)
    # Check if the analyzer returned a successful response
    if response_ia.status_code == 200:
        # Send LLM analyze by email
        # FastAPI returns JSON string .json() converts it to Python object     
        mail = send_mail_to_api(response_ia.json())
        # Print HTTP status code and JSON response from the mail API
        print(mail.status_code)
        print(mail.json())
    else:
        # If analyzer failed, prepare an error message in HTML format
        mail_message = f"<h1>analyze Error</h1><pre>{response_ia.text}</pre>"
         # Send the error message by email
        mail = send_mail_to_api(mail_message)
        print(mail.status_code)
        print(mail.json())
# This block runs only if the script is executed directly
if __name__ == "__main__":
    main()
