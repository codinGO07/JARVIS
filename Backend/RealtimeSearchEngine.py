from googlesearch import search
from groq import Groq # Importing the Groq library to use it
from json import load, dump # Importing functions to read an
import datetime # Importing the datetime module for real-tim
from dotenv import dotenv_values # Importing dotenv_values t

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuratio
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except :
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer
def AnswerModifier(Answer):
    lines = Answer. split('\n') # Split the response into lines.
    non_empty_lines = [line for line in lines if line. strip()] # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines) # Join the cleaned lines back together.
    return modified_answer
SystemChatbot = [
    {'role': 'system','content': System},
    {'role': 'user','content': 'hi'},
    {'role': 'system','content': 'Hello, how may I be of service?'}
]

def Information():
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

def RealtimeSearchEngine(prompt):
    global SystemChatbot, messages

# Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages. append( {"role": "user", "content": f"{prompt}"})

# Add Google search results to the system chatbot messages.
    SystemChatbot.append({"role": "system", "content": GoogleSearch(prompt)})

# Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatbot + [{"role": "system", "content": Information( )} ] + messages,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk. choices[0].delta.content

    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append( {"role": "assistant", "content": Answer})

    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

# Remove the most recent system message from the chatbot con
    SystemChatbot.pop()
    return AnswerModifier(Answer=Answer)

if __name__=="__main__":
    while True:
        print(RealtimeSearchEngine(input(">>>")))
