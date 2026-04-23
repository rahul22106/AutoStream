# AutoStream AI Agent

---

## Project Overview

This is a Conversational AI Agent built for **AutoStream**, a fictional SaaS platform offering automated video editing tools for content creators. The agent is capable of understanding user intent, answering product questions using a RAG pipeline, and capturing high-intent leads through a structured conversation flow.

---

## How to Run the Project Locally

### Prerequisites
- Python 3.11+
- Hugging Face account with API token
- Git

### Step 1 – Clone the Repository
```bash
git clone https://github.com/yourusername/autostream-agent.git
cd autostream-agent
```

### Step 2 – Create Virtual Environment
```bash
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 – Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Set Up Environment Variables
Create a `.env` file in the root directory:
```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

### Step 5 – Run the Agent
```bash
python rag.py
```

---

## Architecture Explanation

The AutoStream agent is built using **LangChain** with a **Mistral-7B-Instruct** model served via Hugging Face Inference API.

The agent is structured around a **LangGraph state graph** that manages conversation flow across multiple turns. Each conversation turn updates a shared state object containing chat history, lead data, and current intent — ensuring memory is retained across 5–6 turns without any external database.

The **RAG pipeline** works by loading a local `knowledge_base.json` file at starting. When a user asks a product or pricing question, relevant sections are extracted using keyword matching and injected into a structured prompt alongside the user query. This allows the model to  response in factual product data, eliminating hallucinations about the questions asked related to the pricing and policies.

**Intent detection** classifies each user message into three categories — greeting, product inquiry, or high-intent lead — using keyword-based logic enhanced by the LLM. When high intent is detected, the agent enters a lead collection flow, gathering name, email, and platform before triggering the `mock_lead_capture()` function. The tool is only triggered after all three values are validated and collected.

---

## 📱 WhatsApp Deployment via Webhooks

To deploy this agent on WhatsApp, the following approach would be used:

1. **Register a WhatsApp Business API** account via Meta Developer Portal and obtain a phone number and access token.

2. **Set up a Webhook endpoint** using a Python web framework like FastAPI. This endpoint receives incoming WhatsApp messages as POST requests from Meta's servers.

3. **Process the message** by extracting the user's text from the webhook payload and passing it to the agent's conversation handler — the same `rag.py` logic.

4. **Send the response back** using the WhatsApp Cloud API by making a POST request to Meta's messages endpoint with the agent's reply.

5. **Deploy the server** on a cloud platform like Railway, Render, or AWS so the webhook URL is publicly accessible and always available.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | LangChain + LangGraph |
| LLM | Mistral-7B-Instruct-v0.2 (Hugging Face) |
| Knowledge Base | Local JSON file (RAG) |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
autostream-agent/
│
├── rag.py                  # Main agent logic
├── knowledge_base.json     # Product knowledge base
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not pushed to GitHub)
├── .gitignore              # Ignores venv and .env
└── README.md               # Project documentation
```

---

## 📦 Dependencies

```
langchain
langgraph
python-dotenv
langchain-community
huggingface_hub==0.36.0
langchain-huggingface==1.2.0
```

---