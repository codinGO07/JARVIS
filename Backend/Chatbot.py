from groq import Groq # Importing the Groq tibrary to use lts API.
from json import load, dump # Importing functions to read and write JSON files.
import datetime # Importing the datetime module for real-time date and time information
from dotenv import dotenv_values # Importing dotenv_values to read environment variable

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username" )
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages=[]
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** Use advance vocabularies and do not repeat the same words. ***
"""
SystemChatBot = [
{"role": "system", "content": System}

]

# Attempt to load the chat log from a JSON file.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f) # Load existing mess
except FileNotFoundError :
# If the file doesn't exist, create an empty
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
def RealtimeInformation():
    current_date_time = datetime.datetime.now() # Get the current date and
    day = current_date_time. strftime("%A") # Day of the week.
    date = current_date_time. strftime("%d") # Day of the month.
    month = current_date_time. strftime("%B") # Full month name.
    year = current_date_time. strftime("%Y") # Year.
    hour = current_date_time. strftime("%H") # Hour in 24-hour format.
    minute = current_date_time.strftime("%M")
    second = current_date_time. strftime("%S")

    # Format the information into a string.
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds. \n"
    return data

def AnswerModifier(Answer):
    lines = Answer. split('\n') # Split the response into lines.
    non_empty_lines = [line for line in lines if line. strip()] # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines) # Join the cleaned lines back together.
    return modified_answer

# Main chatbot function to handle user queries.
def ChatBot(Query):
    try:
    # Load the existing chat log from the JSON file.
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

    # Append the user's query to the messages list.
        messages. append( {"role": "user", "content": f"{Query}"})
        completion = client. chat. completions. create(
                    model="llama3-70b-8192", # Specify the AI model to use.
                    messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation( ) } ] + messages,
                    max_tokens=1024, # Limit the maximum tokens in the response.
                    temperature=0.7, # Adjust response randomness (higher means more random).
                    top_p=1, # Use nucleus sampling to control diversity.
                    stream=True, # Enable streaming response.
                    stop=None # Allow the model to determine when to stop.
                    )

        Answer =""

# Process the streamed response chunks.
        for chunk in completion:
            if chunk. choices[0].delta.content: # Check if there's content in the current chunk.
                Answer += chunk. choices[0].delta.content # Append the content to the answer.

        Answer = Answer.replace("</s>", "") # Clean up any unwanted tokens from the response.

# Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

# Save the updated chat log to the JSON file.
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return AnswerModifier(Answer)
    except Exception as e:
        print(f"An error occurred: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)
    
if __name__=="__main__":
    while True:
        print(ChatBot(input(">>> ")))