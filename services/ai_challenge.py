import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

def get_challenge_feedback(solution_text, challenge, username="Developer"):
    """Get AI feedback on a user's challenge solution using Gemini API
    
    Args:
        solution_text (str): The user's solution to the challenge
        challenge (obj): The challenge object with details
        username (str): The username of the user who submitted the solution
    """
    
    # List of model names to try, in order of preference
    model_names = [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash",
        "models/gemini-2.0-flash-lite",
        "models/gemini-1.5-flash-8b",
    ]
    
    # Create prompt
    prompt = f"""
    A developer named {username} has submitted this solution to the challenge: 
    
    CHALLENGE TITLE: {challenge.title}
    CHALLENGE DESCRIPTION: {challenge.description}
    DIFFICULTY: {challenge.difficulty}
    
    USER'S SOLUTION:
    ```
    {solution_text}
    ```
    
    As a supportive and encouraging mentor, please provide constructive feedback (3-4 sentences) that:
    1. Acknowledges specific strengths in their approach
    2. Provides gentle guidance on areas for improvement
    3. Reinforces their growth mindset to combat imposter syndrome
    4. Includes a small hint if they seem to be struggling or a new challenge if they got it right
    
    Keep your response encouraging and focused on building confidence. Start with a personalized greeting.
    IMPORTANT: Don't mention "imposter syndrome" directly - just be supportive.
    """
    
    # Try each model name until one works
    last_error = None
    for model_name in model_names:
        try:
            # Configure the model
            model = genai.GenerativeModel(model_name)
            
            # Generate response
            print(f"Trying to generate challenge feedback with model: {model_name}")
            response = model.generate_content(prompt)
            
            # Return the generated text
            return response.text
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            last_error = e
            continue
    
    # If we get here, none of the models worked
    print(f"All model attempts failed. Last error: {last_error}")
    return f"Our AI assistant is taking a break, but your solution shows real effort, {username}! Keep exploring different approaches and don't give up."

def generate_new_challenge(difficulty, topic="programming", username="Developer"):
    """Generate a new coding challenge using Gemini AI
    
    Args:
        difficulty (str): beginner, intermediate, or hard
        topic (str): The topic or focus of the challenge
        username (str): The username of the user requesting the challenge
    """
    
    # List of model names to try, in order of preference
    model_names = [
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash",
        "models/gemini-2.0-flash-lite",
        "models/gemini-1.5-flash-8b",
    ]
    
    # Create prompt
    prompt = f"""
    Create a coding challenge for a developer named {username} who is looking for a {difficulty} level challenge on {topic}.
    
    This challenge should:
    1. Be appropriate for their skill level ({difficulty})
    2. Focus on building confidence and overcoming self-doubt
    3. Include clear, achievable goals with a definite solution
    4. Provide 3 progressive hints that help guide without giving away the answer
    
    Format your response with these headers:
    TITLE: (concise, engaging title)
    DESCRIPTION: (clear problem statement and requirements)
    HINTS: (3 progressive hints, from subtle to more direct)
    
    For DESCRIPTION, include any necessary examples, input/output format, and constraints.
    Make the challenge supportive and encouraging - our goal is to help developers build confidence.
    """
    
    # Try each model name until one works
    last_error = None
    for model_name in model_names:
        try:
            # Configure the model
            model = genai.GenerativeModel(model_name)
            
            # Generate response
            print(f"Trying to generate new challenge with model: {model_name}")
            response = model.generate_content(prompt)
            
            # Return the generated text
            return response.text
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            last_error = e
            continue
    
    # If we get here, none of the models worked
    print(f"All model attempts failed. Last error: {last_error}")
    return f"Our AI assistant is taking a break. Please try generating a challenge again later."
