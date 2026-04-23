from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import json
import re
import random

load_dotenv()

# starting by reading my Json file 
with open("knowledge_base.json", "r") as f:
    kb = json.load(f)

# calling the model from HuggingFaceHub
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    max_new_tokens=150,
    do_sample=False,
)

chat = ChatHuggingFace(llm=llm)


lead_data = {}
lead_mode = False
chat_history = []  


# defining the mock lead capture  fuction to collect the name, email and platform details 
def mock_lead_capture(name, email, platform):
    print(f"\nLead captured successfully: {name}, {email}, {platform}\n")

# 
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"h+i+", "hi", text)
    text = re.sub(r"he+y+", "hey", text)
    text = re.sub(r"hello+", "hello", text)
    return text

def clean_name(name):
    name = name.strip()
    name = re.sub(r"(.)\1{2,}", r"\1", name)
    return name.capitalize()

def valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return False

    domain = email.split("@")[1].lower()
    name_part = domain.split(".")[0]

    if re.match(r"^\d+", name_part):
        return False

    trusted = ["gmail.com", "yahoo.com", "outlook.com"]

    return domain in trusted

# fixing of the email from any common errors 
def fix_email_hint(email):
    fixes = {
        "gm.com": "gmail.com",
        "gml.com": "gmail.com",
        "gmil.com": "gmail.com",
        "gmail.comm": "gmail.com"
    }

    try:
        name, domain = email.split("@")
    except:
        return None

    if domain in fixes:
        return f"{name}@{fixes[domain]}"

    if "gmail" in domain and domain != "gmail.com":
        return f"{name}@gmail.com"

    return None

def get_platform(text):
    mapping = {
        "youtube": "youtube",
        "yt": "youtube",
        "instagram": "instagram",
        "insta": "instagram",
        "x": "twitter",
        "twitter": "twitter"
    }
    return mapping.get(text.lower().strip())


def get_intent(user_input):
    text = normalize(user_input)

    if text in ["hi", "hello", "hey"]:
        return "greeting"

    if any(w in text for w in ["want", "try", "interested", "sign up", "pro plan", "basic plan", "upgrade"]):
        return "lead"

    return "info"


def answer_query(user_input):
    context = json.dumps(kb, indent=2)

    history_text = "\n".join(chat_history[-4:])

    prompt = f"""
You are an AI assistant for AutoStream.

Rules:
- Answer only from given data base knowledge provided to you. 
- Keep it under 3 lines
- Do not repeat unnecessary infomation form the knowledge base.
- If you don't know the answer, say Sorry, I don't have that information regard that issue.

Conversation:
{history_text}

Knowledge Base:
{context}

User: {user_input}
Answer:
"""

    res = chat.invoke([HumanMessage(content=prompt)])
    return res.content.strip()


def lead_flow(user_input):
    global lead_data, lead_mode

    if "name" not in lead_data:
        name = clean_name(user_input)

        if len(name) < 2:
            return "That name seems too short."

        lead_data["name"] = name
        return "Cool, what's your email?"

    elif "email" not in lead_data:
        email = user_input.strip().lower()

        hint = fix_email_hint(email)
        if hint:
            return f"Did you mean {hint}?"

        if not valid_email(email):
            return "That email looks invalid. Try Gmail or Outlook."

        lead_data["email"] = email
        return "Which platform do you use? (YouTube, Instagram, etc.)"

    elif "platform" not in lead_data:
        platform = get_platform(user_input)

        if not platform:
            return "Please enter a valid platform like YouTube or Instagram."

        lead_data["platform"] = platform

        mock_lead_capture(
            lead_data["name"],
            lead_data["email"],
            lead_data["platform"]
        )

        lead_data.clear()
        lead_mode = False

        return "You're all set! We'll contact you soon."



print("\nAutoStream Assistant is running (type 'exit' to quit)\n")

greetings = [
    "Hey! How can I help?",
    "Hi there! What can I do for you?",
    "Hello! Need help with something?"
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Bye!")
        break

    chat_history.append(f"User: {user_input}")

    if lead_mode:
        response = lead_flow(user_input)
        print("Bot:", response)
        chat_history.append(f"Bot: {response}")
        continue

    intent = get_intent(user_input)

    if intent == "greeting":
        response = random.choice(greetings)

    elif intent == "lead":
        lead_mode = True
        lead_data.clear()
        response = "Sure, let's get you started. What's your name?"

    else:
        response = answer_query(user_input)

    print("Bot:", response)
    chat_history.append(f"Bot: {response}")