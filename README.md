# 📄 README.md

## Assignment: AI Support Agent (AutoStream)

This project is a conversational AI assistant built for a fictional SaaS product called **AutoStream**. The assistant is designed to handle user queries about the product, explaining plans and policies, and capture leads related to the autostream when users show interest.

The focus of this assignment was to build a simple but functional agent that combines retrieval-based responses with a guided conversation flow.

---

## 🎯 Features Implemented

### 1. Intent Detection
The assistant classifies user input into:
- Greeting (hi, hello, hey, etc.)
- Informational queries (plans, pricing, policies)
- High-intent queries (buy, get plan, subscribe)

This is handled using simple keyword-based logic.

---

### 2. Knowledge-Based Responses (RAG)
- All responses are generated using a local file: `knowledge_base.json`
- The LLM is prompted to only use this data
- This avoids hallucination and keeps answers consistent

---

### 3. Lead Capture Flow
When a user shows interest, the assistant:
1. Asks for name  
2. Asks for email (with validation)  
3. Asks for platform (YouTube, Instagram, etc.)  

After collecting all details, it triggers:

```python
def mock_lead_capture(name, email, platform):

pip install -r requirements.txt

HUGGINGFACEHUB_API_TOKEN=your_token_here

python rag.py