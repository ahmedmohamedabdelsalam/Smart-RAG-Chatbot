# Troubleshooting Guide

Common issues and their solutions for MySmartRAG-Bot.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Connection Problems](#connection-problems)
- [Workflow Execution Errors](#workflow-execution-errors)
- [Performance Issues](#performance-issues)
- [API & Authentication](#api--authentication)

---

## Installation Issues

### n8n Command Not Found

**Symptoms**: `bash: n8n: command not found`

**Solutions**:
```bash
# Option 1: Add npm global to PATH
export PATH="$PATH:$(npm bin -g)"

# Option 2: Reinstall n8n
npm install -g n8n

# Option 3: Use npx
npx n8n start
```

### Python Script Import Errors

**Symptoms**: `ModuleNotFoundError: No module named 'rich'`

**Solution**:
```bash
# Install all requirements
pip install -r requirements.txt

# Or install specific package
pip install rich
```

### Docker Compose Fails

**Symptoms**: Services won't start

**Solutions**:
```bash
# Check Docker is running
docker ps

# View logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up --build -d

# Check port conflicts
netstat -an | findstr "5678"  # Windows
lsof -i :5678  # Linux/Mac
```

---

## Connection Problems

### Cannot Connect to Qdrant

**Symptoms**: `Connection refused` or `Cannot reach Qdrant`

**Diagnostic Steps**:
```bash
# Check if Qdrant is running
curl http://localhost:6333/healthz

# If using Docker
docker ps | grep qdrant

# Check logs
docker logs qdrant
```

**Solutions**:
- Verify QDRANT_URL in `.env` (try `http://127.0.0.1:6333`)
- Restart Qdrant: `docker restart qdrant`
- Check firewall settings
- For cloud Qdrant, verify API key and URL

### n8n Won't Connect

**Symptoms**: `ERR_CONNECTION_REFUSED` when accessing localhost:5678

**Solutions**:
```bash
# Check if n8n is running
curl http://localhost:5678/healthz

# Check port conflicts
netstat -ano | findstr :5678

# Try different port
N8N_PORT=5679 n8n start

# Check logs
journalctl -u n8n  # If using systemd
```

### Webhook URLs Not Working

**Symptoms**: Webhooks return 404 or timeout

**Solutions**:
1. **Check webhook config in n8n**:
   - Ensure "Production URL" is set in Settings
   - Verify webhook path matches

2. **For local development**:
   ```bash
   # Use ngrok or similar
   ngrok http 5678
   # Update WEBHOOK_URL in .env
   ```

3. **For production**:
   - Use proper domain andhttps
   - Configure reverse proxy (nginx)

---

## Workflow Execution Errors

### "Missing Credentials" Error

**Symptoms**: Workflow fails with credential error

**Solutions**:
1. **Add credentials in n8n**:
   - Settings → Credentials
   - Click "New Credential"
   - Select type (OpenAI, Qdrant, etc.)
   - Enter details, test, and save

2. **Reconnect workflow nodes**:
   - Open workflow
   - Click on failed node
   - Select credential from dropdown
   - Save workflow

### Qdrant Collection Not Found

**Symptoms**: `Collection 'xyz' not found`

**Solutions**:
```python
# Create collection manually
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")
client.create_collection(
    collection_name="my_documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)
```

Or let the workflow create it automatically on first run.

### OpenAI Rate Limit Exceeded

**Symptoms**: `Rate limit exceeded` error

**Solutions**:
- Add delays between requests in workflow
- Upgrade OpenAI plan
- Use caching to reduce API calls
- Implement exponential backoff
- Switch to GPT-3.5-turbo (higher limits)

### Workflow Times Out

**Symptoms**: Execution exceeds time limit

**Solutions**:
1. **Increase timeout in n8n**:
   - Workflow settings → Execution timeout
   - Set to higher value (300s default)

2. **Optimize workflow**:
   - Process in smaller batches
   - Use pagination
   - Reduce chunk sizes
   - Cache results

---

## Performance Issues

### Slow Query Responses

**Symptoms**: RAG queries take > 10 seconds

**Optimizations**:
1. **Reduce vector search results**:
   - Lower `top_k` parameter (try 3-5 instead of 10)
   
2. **Optimize chunk size**:
   - Smaller chunks = faster but less context
   - Try 1000-1500 tokens

3. **Use faster embedding model**:
   - `text-embedding-3-small` instead of `large`

4. **Add caching**:
   - Cache common queries
   - Use Redis for embeddings cache

### High Memory Usage

**Symptoms**: System runs out of memory

**Solutions**:
- Process documents in batches
- Limit concurrent workflow executions
- Increase Docker memory limit:
  ```yaml
  services:
    n8n:
      mem_limit: 2g
  ```
- Use streaming for large files
- Clear old execution data regularly

### Database Growing Too Large

**Solutions**:
```sql
-- Clean old n8n executions
DELETE FROM execution_entity 
WHERE "stoppedAt" < NOW() - INTERVAL '30 days';

-- Optimize PostgreSQL
VACUUM ANALYZE;
```

For Qdrant:
```python
# Delete old points
client.delete(
    collection_name="my_docs",
    points_selector=FilterSelector(
        filter=Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=DatetimeRange(lt=datetime.now() - timedelta(days=90))
                )
            ]
        )
    )
)
```

---

## API & Authentication

### Invalid OpenAI API Key

**Symptoms**: `401 Unauthorized` from OpenAI

**Solutions**:
- Verify key is correct (starts with `sk-`)
- Check for spaces in `.env` file
- Ensure key has required permissions
- Check billing is active
- Generate new key if compromised

### Gemini API Errors

**Symptoms**: Authentication or quota errors

**Solutions**:
- Verify API key from Google AI Studio
- Check API is enabled in Google Cloud
- Review quota limits
- Use correct model name (`gemini-2.0-flash-exp`)

### Telegram Bot Not Responding

**Symptoms**: Bot doesn't reply to messages

**Solutions**:
1. **Check bot token**:
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
   ```

2. **Verify webhook**:
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo
   ```

3. **Set webhook manually**:
   ```bash
   curl -F "url=https://yourdomain.com/webhook/telegram" \
        https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook
   ```

---

## Common Error Messages

### `ECONNREFUSED`
**Meaning**: Connection refused
**Fix**: Service not running or wrong URL/port

### `ETIMEDOUT`
**Meaning**: Request timeout
**Fix**: Increase timeout, check network, verify service is responding

### `EADDRINUSE`
**Meaning**: Port already in use
**Fix**: Stop other service or use different port

### `Error: Invalid JSON`
**Meaning**: Malformed workflow file
**Fix**: Validate JSON syntax, use `npm run validate`

### `Cannot find module`
**Meaning**: Missing dependency
**Fix**: Run `pip install -r requirements.txt`

---

## Getting Further Help

If issues persist:

1. **Check logs**:
   ```bash
   # n8n logs
   docker logs n8n
   
   # Qdrant logs
   docker logs qdrant
   
   # Python script with debug
   python -v scripts/script_name.py
   ```

2. **Enable debug mode**:
   ```env
   LOG_LEVEL=DEBUG
   N8N_LOG_LEVEL=debug
   ```

3. **Search existing issues**:
   - [GitHub Issues](https://github.com/YOUR_USERNAME/Smart-RAG-Chatbot/issues)
   - [n8n Community Forum](https://community.n8n.io/)

4. **Create new issue** with:
   - Detailed description
   - Steps to reproduce
   - Error logs
   - Environment details (OS, versions)

---

**Still stuck?** Open an issue on [GitHub](https://github.com/YOUR_USERNAME/Smart-RAG-Chatbot/issues)
