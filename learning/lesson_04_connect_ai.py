# Read a secret without displaying it in the Terminal.
from getpass import getpass
# Import the client provided by the OpenAI Python library.
from openai import OpenAI

# Ask for your API key.
api_key = getpass("Paste your OpenAI API key, then press Enter: ")
# Create an object that lets our program communicate with OpenAI.
client = OpenAI(api_key=api_key)

print("Sending your question to the AI ")

# Send the instruction and wait for the model's response.
response = client.responses.create(
    model ="gpt-4.1-mini",
    input ="Explain what a percentage means in two simple sentences .",
    max_output_tokens =150  #A limit on generated tokens; tokens are pieces of text, not necessarily whole words
)

# Display the text from the response.
print(" \n AI response :")
print(response.output_text)
