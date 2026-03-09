# Workflow Usage Guide

This guide provides detailed information on how to use and configure the workflows included in **MySmartRAG-Bot**.

## RAG Chatbots

### [Chatbot RAG Google Drive Gemini](workflows/rag-chatbots/chatbot_rag_google_drive_gemini.json)
- **Description**: A powerful chatbot that can answer questions based on documents stored in a Google Drive folder.
- **Setup**:
  1. Set up Google Drive credentials in n8n.
  2. Provide the `Folder ID` in the Google Drive node.
  3. Configure Qdrant credentials and collection name.
- **Usage**: Once documents are indexed, the chatbot will use Gemini to provide answers grounded in your data.

### [Telegram Chatbot Session-Based](workflows/rag-chatbots/chatbot_telegram_session_based.json)
- **Description**: A conversational bot for Telegram that remembers context using Google Sheets as a light memory store.
- **Setup**:
  1. Create a Telegram bot via @BotFather.
  2. Add the token to `.env` or n8n credentials.
  3. Create a Google Sheet for session storage.
- **Usage**: Message the bot on Telegram; it will maintain a cohesive conversation thread.

---

## Document Processing

### [PDF Image Extraction Gemini](workflows/document_processing/pdf_image_extraction_gemini.json)
- **Description**: Uses Gemini's multi-modal capabilities to extract text and structured data from complex PDFs and images.
- **Setup**: 
  1. Configure Gemini 2.0 Flash credentials.
  2. Point the file node to your input source.
- **Usage**: Automatically identifies tables, headers, and key entities in documents.

### [LlamaParse Document Extraction](workflows/document_processing/llamaparse_document_extraction.json)
- **Description**: High-fidelity PDF parsing using LlamaParse, optimized for complex layouts.
- **Setup**: Requires a LlamaIndex API key.
- **Usage**: Input a PDF, receive structured Markdown output ideal for RAG indexing.

---

## AI Agents

### [AI Agent Long Term Memory](workflows/ai_agents/ai_agent_long_term_memory.json)
- **Description**: An autonomous agent that can take notes and retrieve them later, simulating a long-term memory.
- **Setup**: Connects to a vector database for note storage.
- **Usage**: Command the agent to "Remember that I like blue" and later ask "What color do I like?".

### [AI Agent RAG Multi-Tenant Supabase](workflows/ai_agents/ai_agent_rag_multi_tenant_supabase.json)
- **Description**: Advanced agent implementation supporting multiple users with isolated document stores.
- **Setup**: Requires Supabase with pgvector enabled.
- **Usage**: Ideal for SaaS applications where each user manages their own knowledge base.

---

## Integrations

### [Semantic Web Search Re-Rank](workflows/integrations/semantic_web_search_re_rank.json)
- **Description**: Enhances web search results using a cross-encoder re-ranking model for higher accuracy.
- **Setup**: Uses SearchAPI or Brave Search alongside a re-ranking model (Cohere or similar).
- **Usage**: Get the most relevant snippets from the web for complex queries.

### [Jina AI Deep Research Agent](workflows/integrations/jina_ai_deep_research_agent.json)
- **Description**: A specialized agent for conducting deep web research on any topic.
- **Setup**: Configure Jina AI and Brave Search credentials.
- **Usage**: Provide a research topic; the agent will scrape, summarize, and compile a report.

---

## Utilities

### [n8n Local AI](workflows/utilities/n8n_local_ai.json)
- **Description**: Template for using local LLMs (Ollama/LM Studio) with n8n.
- **Setup**: Ensure your local LLM server is running and accessible (default port 11434).
- **Usage**: Run RAG workflows without sending data to external cloud providers.

---

## Best Practices for All Workflows

1. **Credentials First**: Before running any imported workflow, go to **Settings > Credentials** and ensure all required services are authenticated.
2. **Environment Variables**: Use the `.env` file for values that change between environments (URLs, fixed IDs).
3. **Trigger Testing**: For webhook-based workflows, always run the "Test" execution once to ensure the webhook is active.
4. **Monitoring**: Regularly check the n8n **Executions** tab to debug failed nodes and monitor performance.

---

Developed by **Ahmed Abdelsalam**
