import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def get_ai_feedback(win_content, username="Developer"):
    """Get AI feedback on a user's daily win using Gemini API
    
    Args:
        win_content (str): The content of the user's win
        username (str): The username of the user who submitted the win
    """
    
    # List of model names to try, in order of preference
    # Based on the available models in the account
    model_names = [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash",
        "models/gemini-2.0-flash-lite",
        "models/gemini-1.5-flash-8b",
    ]
    
    # Create prompt
    prompt = f"""
    A developer named {{ user.username }} has shared this achievement: 
    
    "{win_content}"
    
    As a supportive and uplifting mentor, provide encouraging, personalized feedback (2-3 sentences) 
    that acknowledges their achievement, reinforces their growth mindset, and offers gentle guidance 
    for continued improvement. Start with "That's fantastic, {{ user.username }}!" or a similar personalized greeting.
    Focus on building their confidence and helping them overcome impostor syndrome.
    """
    
    # Try each model name until one works
    last_error = None
    for model_name in model_names:
        try:
            # Configure the model
            model = genai.GenerativeModel(model_name)
            
            # Generate response
            print(f"Trying to generate content with model: {model_name}")
            response = model.generate_content(prompt)
            
            # Return the generated text
            return response.text
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            last_error = e
            continue
    
    # If we get here, none of the models worked
    print(f"All model attempts failed. Last error: {last_error}")
    return f"Our AI assistant is taking a break, but your win is still amazing, {username}! Keep up the great work."
