# Frequently Asked Questions (FAQ)

## General Questions

### What is MySmartRAG-Bot?
MySmartRAG-Bot is a collection of production-ready n8n workflows that implement Retrieval-Augmented Generation (RAG) for building intelligent chatbots, document processing systems, and AI agents.

### Do I need programming experience?
Basic familiarity with APIs and configuration files is helpful, but the interactive setup wizard and comprehensive documentation make it accessible to beginners. Most workflows can be used without coding.

### Is this free to use?
Yes! The project is open-source under MIT License. However, you'll need API keys for services like OpenAI (paid), Gemini (free tier available), and vector databases.

---

## Installation & Setup

### Which installation method should I use?
- **Docker Compose**: Best for production and easiest setup
- **Quick Install**: Best for development and testing
- **Manual Install**: Best if you already have services running

### Do I need all the API keys?
No. Only OpenAI API key is essential for most workflows. Other keys (Gemini, Telegram, etc.) are optional and depend on which workflows you want to use.

### Can I use local LLMs instead of OpenAI?
Yes! Check the `n8n_local_ai.json` workflow in `workflows/utilities/` for local LLM integration examples.

###How much does it cost to run?
- **n8n**: Free (open-source)
- **Qdrant**: Free for local, cloud has free tier
- **OpenAI API**: Pay-per-use (~$0.002-0.03 per 1K tokens)
- **Infrastructure**: Free locally, $10-50/month cloud depending on usage

---

## Workflows

### How do I choose the right workflow?
- **Simple chatbot**: Start with "Telegram Chatbot Session-Based"
- **Document Q&A**: Use "RAG Chatbot with Google Drive"
- **Web search**: Try "Web Search Chatbot with Brave"
- **PDF processing**: Use "PDF Extraction with Claude"

### Can I modify the workflows?
Absolutely! All workflows are fully customizable. Clone the workflow in n8n and modify nodes, prompts, and logic as needed.

### How do I create my own workflow?
1. Study existing workflows to understand patterns
2. Use n8n's visual editor to create nodes
3. Follow the structure in `docs/ARCHITECTURE.md`
4. Save as JSON and add to appropriate category

### Why do some workflows fail?
Common reasons:
- Missing or invalid API keys
- Credentials not configured in n8n
- Vector database not running
- Incorrect webhook URLs
- Rate limits exceeded

---

## Vector Databases & RAG

### What is RAG?
Retrieval-Augmented Generation combines semantic search (retrieving relevant information) with language models (generating responses) to create accurate, context-aware chatbots.

### Do I need Qdrant specifically?
No. While we use Qdrant in examples, you can use:
- Supabase Vector (with PostgreSQL)
- Pinecone
- Weaviate
- ChromaDB

### How do I add documents to the vector database?
Use workflows like "RAG Chatbot with Google Drive" which:
1. Extract text from documents
2. Split into chunks
3. Create embeddings
4. Store in vector database

### What's the best chunk size?
- **Short documents**: 500-1000 tokens
- **Long documents**: 1500-3000 tokens
- **Technical docs**: 1000-2000 tokens
Start with 2000 and adjust based on results.

---

## Troubleshooting

### Workflows import but credentials are missing
After import:
1. Go to Settings → Credentials in n8n
2. Add your OpenAI, Gemini, Qdrant credentials
3. Open each workflow and reconnect nodes to credentials

### Vector database queries return no results
Check:
- Are documents actually in the collection? (`collection.count()`)
- Is the embedding model same for indexing and querying?
- Try lower similarity threshold (0.5 instead of 0.8)
- Verify collection name matches in workflow

### n8n execution times out
- Increase timeout in n8n settings
- Reduce document chunk size
- Use faster embedding models
- Process documents in smaller batches

### High API costs
Optimize:
- Use caching for repeated queries
- Implement rate limiting
- Use GPT-3.5-turbo instead of GPT-4
- Reduce chunk overlap
- Cache embeddings

---

## Best Practices

### How often should I backup workflows?
- Before major changes
- After creating new workflows
- Weekly for production systems
Use: `python scripts/backup_workflows.py create`

### How do I version control my workflows?
workflows are JSON files, use Git:
```bash
git add workflows/
git commit -m "feat: Add new chatbot workflow"
git push
```

### Should I use webhooks or polling?
- **Webhooks**: Real-time, efficient (recommended)
- **Polling**: Simpler setup, less efficient
For chatbots, use webhooks.

### How do I secure my API keys?
- Never commit `.env` file
- Use environment variables
- Rotate keys regularly
- Implement rate limiting
- Use n8n's built-in credential encryption

---

## Integration

### Can I integrate with my existing app?
Yes! n8n workflows can:
- Expose webhook endpoints
- Connect to databases
- Call external APIs
- Use websockets

### How do I add Telegram integration?
1. Create bot with @BotFather
2. Get bot token
3. Add to `.env` file
4. Configure in n8n credentials
5. Use Telegram node in workflows

### Can I use with Discord/Slack?
Yes! n8n has nodes for both. Follow similar pattern to Telegram workflows.

---

## Performance

### How many concurrent users can it handle?
Depends on your infrastructure:
- **Local**: 5-10 concurrent users
- **Cloud (small)**: 50-100 users
- **Cloud (scaled)**: 1000+ users with proper architecture

### How do I scale the system?
1. Use Docker Compose with replicas
2. Add Redis for caching
3. Use queue system for heavy tasks
4. Horizontal scaling of n8n instances
5. Dedicated vector database cluster

### What's the response time?
Typical:
- Simple query: 1-3 seconds
- RAG query: 2-5 seconds
- Document processing: 10-30 seconds
Optimize with caching and faster models.

---

## Advanced Topics

### Can I train custom models?
This project uses API-based models (OpenAI, Gemini). For custom models:
- Fine-tune OpenAI models via API
- Use local LLMs (see `n8n_local_ai.json`)
- Self-host models with vLLM/Ollama

### How do I implement multi-tenancy?
See "AI Agent RAG Multi-Tenant Supabase" workflow for example using:
- User identification
- Separate collections per tenant
- Row-level security
- Metadata filtering

### Can I add authentication?
Yes:
- Enable n8n basic auth
- Use API keys for webhooks
- Implement JWT authentication
- Integrate with OAuth providers

---

## Support

### Where can I get help?
1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/YOUR_USERNAME/MySmartRAG-Bot/issues)
3. Join n8n community forum
4. Open a new issue

### How do I report bugs?
Open an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Workflow JSON (if relevant)
- Error logs

### Can I hire you for custom development?
Contact via the repository for custom workflow development and consulting.

---

**More questions?** Open an issue or check the [documentation](.).
