import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def get_daily_boost(username="Developer"):
    """Generate an enhanced daily boost with inspiring quote and personal growth challenge
    
    Args:
        username (str): The username of the user
        
    Returns:
        dict: A dictionary containing the generated quote and challenge
    """
    
    # List of model names to try, in order of preference
    model_names = [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash",
        "models/gemini-2.0-flash-lite", 
        "models/gemini-1.5-flash-8b",
    ]
    
    prompt = f"""
    You are a personal growth coach for developers. Generate an inspiring daily boost for a developer
    named {username}. The boost should contain:
    
    1. An inspiring quote about growth, learning, overcoming challenges, or building confidence.
    The quote should be attributed to its author.
    
    2. A short, actionable challenge for personal or professional growth that can be completed in a day.
    The challenge should help with skills development, creative thinking, or overcoming impostor syndrome.
    
    Format your response as a JSON object with the following structure:
    {{
        "quote": "The inspiring quote goes here.",
        "author": "Quote Author",
        "challenge": "The daily challenge description goes here."
    }}
    
    Make sure the quote is genuinely inspiring and the challenge is specific and achievable.
    """
    
    # Try each model name until one works
    last_error = None
    for model_name in model_names:
        try:
            # Configure the model
            model = genai.GenerativeModel(model_name)
            
            # Generate response
            print(f"Trying to generate daily boost with model: {model_name}")
            response = model.generate_content(prompt)
            
            # Return the generated text
            result_text = response.text
            
            # Clean up the response to extract the JSON portion
            import json
            # Find JSON in the text (it might be surrounded by backticks or other text)
            import re
            json_match = re.search(r'({.*})', result_text.replace('\n', ' '))
            if json_match:
                try:
                    result_json = json.loads(json_match.group(1))
                    return result_json
                except json.JSONDecodeError:
                    # If JSON parsing fails, fallback to default
                    pass
            
            # Fallback - return default in case JSON parsing failed
            return {
                "quote": "The journey of a thousand miles begins with a single step.",
                "author": "Lao Tzu",
                "challenge": "Take 30 minutes today to learn something new in your programming language of choice."
            }
            
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            last_error = e
            continue
    
    # If we get here, none of the models worked
    print(f"All model attempts failed. Last error: {last_error}")
    return {
        "quote": "The journey of a thousand miles begins with a single step.",
        "author": "Lao Tzu",
        "challenge": "Take 30 minutes today to learn something new in your programming language of choice."
    }
