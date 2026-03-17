
from litellm import completion, AuthenticationError, RateLimitError, APIError 
from fastapi import HTTPException
import os

# Function to send log text to the LLM and get the analysis result
def analyze_log(log_text: str):
    api_key = os.getenv("api_key")    
    try:
        # Send request to the LLM
        response = completion(
            model="gemini/gemini-2.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyse ces logs et répond uniquement en JSON :\n{log_text}"        
                }            
            ],
            api_key=api_key
        )
        # Return the model response content
        return response.choices[0].message.content
    
    
    # Catch LiteLLM exception and raises FastApI Exception with LiteLLM Exception message
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Catch any other exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    