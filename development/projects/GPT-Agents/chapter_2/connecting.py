import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
api_base = os.getenv('OPENAI_API_BASE')
model_name = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')

# Ensure the API key is available
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

# Initialize the client with base URL
client = OpenAI(
    base_url=api_base,
    api_key=api_key
)

# Example function to query ChatGPT
def ask_chatgpt(user_message):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": user_message}],
        temperature=0.7,
    )       
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    user = "На какой архитектуре используется модель deepseek-r1-0528-qwen3-8b?"
    try:
        response = ask_chatgpt(user)
        print("Response:", response)
    except Exception as e:
        print(f"Error: {str(e)}")
