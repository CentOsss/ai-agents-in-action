from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # loading and setting the api key can be done in one step


# Example function to query ChatGPT
def prompt_llm(messages, 
               model="gpt-4o-mini", 
               base_url="https://api.proxyapi.ru/openai/v1", 
               api_key="sk-Cpt0I1HB2rNekF9PNwxLOdFv0ewHdqp4"):
    if base_url:
        #Azure or local LLM deployment
        client = OpenAI(base_url=base_url, api_key=api_key)
    else:
        #OpenAI deployment, api key set in environment variable
        client = OpenAI() # This branch might not be used anymore if base_url is always provided
        
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,                
        )       
    
    return response.choices[0].message.content