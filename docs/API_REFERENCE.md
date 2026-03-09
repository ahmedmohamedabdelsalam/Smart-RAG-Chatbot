# API Reference

**MySmartRAG-Bot** workflows can be triggered and interacted with via their exposed API endpoints. This document details the standard interfaces and payload structures.

## Authentication

All production endpoints should be protected. n8n supports several methods:
- **Header Auth**: Add an `X-API-KEY` header to your requests.
- **Basic Auth**: Standard username/password authentication.
- **JWT**: For advanced integration with external auth providers.

## Standard Webhook Endpoints

### 1. Chatbot Webhook
Exposed by workflows in `workflows/rag-chatbots/`.

- **Endpoint**: `https://your-n8n-instance/webhook/chatbot`
- **Method**: `POST`
- **Payload**:
```json
{
  "query": "What are the company's Q3 goals?",
  "userId": "user_123",
  "sessionId": "abc-789"
}
```
- **Response**:
```json
{
  "response": "Based on the documents in Google Drive, the Q3 goals are...",
  "sources": [
    {"name": "q3_strategy.pdf", "relevance": 0.95}
  ]
}
```

### 2. Document Indexing Trigger
Used to trigger a re-index of documents.

- **Endpoint**: `https://your-n8n-instance/webhook/index-documents`
- **Method**: `POST`
- **Payload**:
```json
{
  "action": "refresh",
  "folderId": "gdrive_folder_id_optional"
}
```

## Utility Script API (CLI)

The Python utility scripts provide a command-line interface for internal system management.

### Setup Wizard
```bash
python scripts/setup_wizard.py
```
*Guides the user through setting up the `.env` file.*

### Workflow Validator
```bash
python scripts/workflow_validator.py --check-all
```
*Returns a JSON-compatible report of all workflow health.*

### Workflow Importer
```bash
python scripts/workflow_importer.py --category <category_name>
```
*API-based bulk import to n8n.*

## Connection Parameters

When integrating externally, ensure these parameters match your deployment:

| Variable | Default | Description |
|----------|---------|-------------|
| `N8N_HOST` | `localhost` | Hostname of your n8n instance |
| `N8N_PORT` | `5678` | Listening port for n8n |
| `QDRANT_URL` | `http://localhost:6333` | Vector database endpoint |
| `REDIS_URL` | `redis://localhost:6379` | Caching layer endpoint |

---

Developed by **Ahmed Abdelsalam**
