import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_ai_feedback(win_content):
    """Get AI feedback on a user's daily win using Gemini API"""
    
    # Configure the model
    model = genai.GenerativeModel('gemini-pro')
    
    # Create prompt
    prompt = f"""
    A junior developer has shared this achievement: 
    
    "{win_content}"
    
    As a supportive and uplifting mentor, provide encouraging, personalized feedback (2-3 sentences) 
    that acknowledges their achievement, reinforces their growth mindset, and offers gentle guidance 
    for continued improvement. Focus on building their confidence and helping them overcome 
    impostor syndrome.
    """
    
    # Generate response
    response = model.generate_content(prompt)
    
    # Return the generated text
    return response.text