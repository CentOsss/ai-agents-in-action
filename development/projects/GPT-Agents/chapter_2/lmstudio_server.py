from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://172.21.144.1:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="llama-2-7b-chat", # this field is currently unused
  messages=[
    {"role": "system", "content": "Always answer in russian."},
    {"role": "user", "content": "Столица России?"}
  ],
  temperature=0.7,
)

print(completion.choices[0].message)