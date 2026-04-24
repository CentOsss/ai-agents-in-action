from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://172.21.144.1:4891/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="meta-llama-3-8b-instruct", # this field is currently unused
  messages=[
    {"role": "system", "content": "Always answer in russian."},
    {"role": "system", "content": "I want to create a GPT assistant that can generate a FastAPI service that will perform some action to be specified. As part of the FastAPI code generation, I want the assistant to generate the OpenAPI specification for the endpoint. Please outline a set of instructions for this agent"}
  ],
  temperature=0.7,
)

print(completion.choices[0].message)