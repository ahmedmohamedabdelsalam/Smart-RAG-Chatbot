# Smart-RAG-Chatbot

**A smart website chatbot using Retrieval-Augmented Generation (RAG) with n8n workflows, OpenAI embeddings, and a vector database for intelligent, real-time responses. Developed by Ahmed Mohamed Abdelsalam.**

---

## Overview

This repository contains a collection of n8n workflows implementing Retrieval-Augmented Generation (RAG) for AI-powered workflow automation. It provides ready-to-deploy workflows and reference examples for creating intelligent chatbots, document question-answering systems, and real-time conversational agents.

---

## Repository Structure

```
.
├── workflows/                   # Main n8n workflow JSON files
├── documentation/               # Optional documentation datasets for RAG
├── scripts/                     # Python or JS utility scripts
├── config/                      # Environment configuration templates
├── README.md                    # Project documentation
└── requirements.txt             # Python dependencies
```

---

## Features

- Automated content extraction from websites and internal documents
- Semantic search using embeddings for accurate, context-aware answers
- Real-time conversational AI chatbot integration for websites
- API endpoints for easy integration with any website
- Multi-source document support with chunking and metadata filtering
- Scalable architecture using n8n workflows and vector databases

---

## Tech Stack

- **n8n Workflows** – workflow orchestration and automation
- **OpenAI Embeddings** – semantic search and knowledge representation
- **Vector Database** – Qdrant, Pinecone, or Supabase Vector DB
- **Python / Node.js** – for workflow utilities and LLM integrations
- **HTML/CSS/JS** – optional for front-end website integration

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Smart-RAG-Chatbot.git
cd Smart-RAG-Chatbot
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables (`.env`):

```
OPENAI_API_KEY=your_openai_api_key
VECTOR_DB_URL=your_vector_database_url
```

4. Import n8n workflows:

- Open n8n dashboard
- Import JSON workflow files from the `workflows/` folder
- Connect credentials (OpenAI, Vector DB, etc.)

---

## Usage

- Start n8n: 

```bash
n8n start
```

- Trigger workflows via:

  - Webhooks
  - Scheduled executions
  - Manual activation
  - API calls

- The workflows will automatically handle:

  1. Content extraction
  2. Embeddings creation and storage in the vector database
  3. Answering user queries through the chatbot interface or API

---

## Performance Considerations

- RAG queries typically complete in 2–5 seconds depending on complexity
- Workflow generation may take 10–30 seconds for complex cases
- Consider batch processing for high-volume operations

---

## Learning Resources

- [n8n Official YouTube Tutorials](https://www.youtube.com/c/n8n-io)
- [n8n Documentation](https://docs.n8n.io/)
- [Webhook Guide for Self-Hosting](https://docs.n8n.io/workflows/trigger-nodes/webhook/)

---

## Credits

Developed entirely by **Ahmed Mohamed Abdelsalam** as part of AI projects and portfolio.

---

## License

This project is open for personal and educational use. Modify and use it freely for your own projects.
