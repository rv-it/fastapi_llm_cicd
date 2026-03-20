
from litellm import completion, AuthenticationError, RateLimitError, APIError 
from fastapi import HTTPException
import os

# Function to send log text to the LLM and get the analysis result
def analyze_log(log_text: str, model: str):
    api_key = os.getenv("api_key")    
    try:
        # Send request to the LLM
        response = completion(
            model=model,
            # Message to define LLM behavior and send logs
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Je vais te donner un ou des logs journalctl à analyser, répond en anglais avec un HTML valide et propre car ta réponse sera transmise par mail via script python (lib smtplib et EmailMessage).            
                    Le seuil de détection est defini à partir de warning, commence par quelquechose du type "un incident s'est produit sur votre serveur (nom du serveur)".
                    Après affiche le log, le nombre d'occurence si besoin, des pistes de diagnostique, tout ce qui te semble pertinent avec une présentation la plus propre possible.
                    Voiçi les logs  :\n{log_text}
                    """        
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
    