
from litellm import completion, AuthenticationError, RateLimitError, APIError 
from dotenv import load_dotenv
from fastapi import HTTPException
import os


def analyze_log(log_text: str):
    api_key = os.getenv("api_key")
    
    try:
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
        return response.choices[0].message.content
    
    # si print(e) ça va s'afficher juste dans le terminal ou tourne uvicorn, pas dans le terminal ou est lancé le script (tout va semblé fonctionner comme l'API fast api marche).
    # return e ça va afficher l'erreur mais garde code 200 (car l'api fonctionne c'est le backend Litellm qui merde), HTTPException pour gerer correctement les erreurs (doc fastapi)
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    