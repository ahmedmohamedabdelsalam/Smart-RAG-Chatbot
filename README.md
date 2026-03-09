---
title: Smart RAG Chatbot
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Smart RAG Chatbot 
*A Production-Ready Retrieval-Augmented Generation (RAG) Assistant*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Generative%20AI-orange)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=huggingface)

**[🚀 Try the Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Abdelsalam-1/Smart-RAG-Chatbot)**

Are you looking for an AI agent that doesn't just "talk", but actually *knows* about you or your business? You've found the right repository.

This project is a high-performance, robust, and beautifully designed **RAG (Retrieval-Augmented Generation)** Web Application. It ingests custom text data, embeds it into a Vector Database, and leverages **Google Gemini** to answer user queries backed by your specific context. 

---

## Key Features
- **Local Data Ingestion:** Automatically reads and parses `data.txt` on startup, converting the text into dense vectors for intelligent context retrieval. You can place your CV, business FAQs, or documentation inside!
- **Blazing Fast API:** Built natively with **FastAPI**, establishing robust endpoints for health checks and AI completions.
- **Premium UI/UX:** A sleek, mobile-responsive **Glassmorphism** aesthetic frontend. Includes a sidebar for session-persistent chat history (via LocalStorage) and typing animations.
- **Auto-Bilingual:** Automatically detects the user's browser language. Supports LTR (English) and RTL (Arabic) natively on the fly.
- **Production Ready:** Fully containerized via `Dockerfile` and includes deployment YAML blueprints for one-click cloud deployment.

---

## Architecture
1. **Frontend:** Vanilla HTML/CSS/JS providing a seamless SPA-like chat experience without the heavy node_modules overhead.
2. **Backend API:** FastAPI serving both the static UI and the JSON endpoints. 
3. **Embeddings & LLM:** Google Gemini (`gemini-2.5-flash` for blazing-fast inference and `text-embedding-004` for semantic context matching).
4. **Vector Database:** **Qdrant**. Automatically configured to run `In-Memory` for instant zero-configuration local deployments, while seamlessly supporting remote Qdrant Cloud connections via the `.env`.

---

## Quick Start (Local Setup)

### 1. Clone & Install
```bash
git clone https://github.com/YourUsername/Smart-RAG-Chatbot.git
cd Smart-RAG-Chatbot
python -m venv .venv
# Activate the environment (Windows)
.venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file from the provided template:
```bash
cp .env.example .env
```
Open `.env` and add your [Google AI Studio Key](https://aistudio.google.com/):
`GOOGLE_GEMINI_API_KEY=your_key_here`

### 3. Add Custom Data (Optional but Recommended)
Open the `data.txt` file in the root directory and paste your Resume/CV, or any specific knowledge you want the bot to know.

### 4. Run the Server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
Visit `http://localhost:8000/` in your browser.

---

## Docker Deployment
This project is containerized for maximum portability.
```bash
docker build -t smart-rag-chatbot .
docker run -p 8000:8000 --env-file .env smart-rag-chatbot
```

---

## Author Profile
Built passionately by an AI & Backend Engineer dedicated to crafting intelligent and scalable software systems. If you're a recruiter testing this agent, feel free to ask the chatbot about my skills and experience—it knows my `data.txt` cover to cover!

*If you liked this project, don't forget to give it a star!*
