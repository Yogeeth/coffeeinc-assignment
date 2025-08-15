#  Simple Chat - Streamlit + Ollama LLM Interface

A **Streamlit-based chat interface** to interact with **local Large Language Models (LLMs)** using [Ollama](https://ollama.ai/).  
It allows you to **download, manage, and switch models**, maintain **multiple chat sessions**, and **stream AI responses in real-time**.

---

## Features

- **Model Management**
  - Download popular or custom models directly from the UI.
  - View available locally installed models.
  - Switch between models instantly.

- **Multi-Chat Sessions**
  - Create multiple independent chat sessions.
  - Each chat maintains its own conversation memory.
  - First user message is used as chat title.

- **Real-Time Streaming**
  - See AI’s response as it’s being generated.
  - Maintains conversation context 

- **Chat History**
  - Sidebar navigation for saved chats.
  - Option to delete old chats.

---

##  Requirements

- **Python** 3.8+
- **Ollama** installed locally ([Installation Guide](https://ollama.ai/download))
- Models pulled via Ollama CLI or the in-app download interface.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yogeeth/coffeeinc-assignment.git
   cd simple-chat-ollama
   pip install -r requirements.txt
   streamlit run app.py
   cd coffeeinc-assignment
   cd Task2
   code . (optional)

## 🖥️ UI Overview

### **Sidebar**
- Download models (popular & custom)
- Select model
- Create new chat
- Browse & delete chat history

### **Main Area**
- Displays current chat messages
- Chat input box
- Model download interface (when needed)



