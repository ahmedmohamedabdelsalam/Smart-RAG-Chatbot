# Installation Guide

This guide will walk you through setting up the MySmartRAG-Bot project from scratch.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Installation](#quick-installation)
- [Docker Installation](#docker-installation)
- [Manual Installation](#manual-installation)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18.0.0 or higher ([Download](https://nodejs.org/))
- **Python** 3.8 or higher ([Download](https://python.org/))
- **npm** 9.0.0 or higher (comes with Node.js)
- **Git** ([Download](https://git-scm.com/))

### Recommended
- **Docker** & **Docker Compose** (for containerized setup)
- **VS Code** or similar code editor

### Required API Keys
- **OpenAI API Key** (required for most workflows)
- **Google Gemini API Key** (optional, for Gemini-based workflows)
- **Qdrant** instance (local or cloud)

---

## Quick Installation

The fastest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/MySmartRAG-Bot.git
cd MySmartRAG-Bot

# 2. Install dependencies
pip install -r requirements.txt
npm install

# 3. Run interactive setup
python scripts/setup_wizard.py

# 4. Start n8n
n8n start

# 5. Import workflows
python scripts/workflow_importer.py

# 6. Validate setup
npm run validate
```

---

## Docker Installation

### Using Docker Compose (Recommended)

1. **Copy the Docker Compose file**
   ```bash
   cp examples/docker-compose.yml docker-compose.yml
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Access n8n**
   - Open browser to `http://localhost:5678`
   - Create your n8n account
   - Import workflows manually or via script

### What Docker Compose Includes

- **n8n** - Workflow automation platform
- **Qdrant** - Vector database (localhost:6333)
- **PostgreSQL** - n8n database
- **Redis** - Caching layer

---

## Manual Installation

### Step 1: Install n8n

```bash
# Global installation
npm install n8n -g

# Or local installation
npm install n8n --save
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Qdrant Vector Database

#### Option A: Qdrant Cloud (Recommended for Production)
1. Sign up at [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a cluster
3. Copy your API key and URL

#### Option B: Local Qdrant with Docker
```bash
docker run -p 6333:6333 qdrant/qdrant
```

#### Option C: Local Qdrant Binary
Download from [Qdrant Releases](https://github.com/qdrant/qdrant/releases)

### Step 4: Configure Environment

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
OPENAI_API_KEY=sk-...
GOOGLE_GEMINI_API_KEY=...
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty for local
```

---

## Configuration

### Interactive Setup Wizard

Run the setup wizard for guided configuration:

```bash
python scripts/setup_wizard.py
```

This will:
- Collect your API keys securely
- Test connections to services
- Generate .env file
- Provide next steps guidance

### Manual Configuration

Edit `.env` file directly:

```env
# Essential
OPENAI_API_KEY=your_key_here
QDRANT_URL=http://localhost:6333

# n8n
N8N_HOST=localhost
N8N_PORT=5678

# Optional integrations
TELEGRAM_BOT_TOKEN=your_token
GOOGLE_DRIVE_CLIENT_ID=your_client_id
```

### n8n Configuration

1. **Start n8n**
   ```bash
   n8n start
   ```

2. **Access dashboard**
   - URL: `http://localhost:5678`
   - Create account on first visit

3. **Add credentials in n8n**
   - Settings → Credentials
   - Add OpenAI, Gemini, Qdrant credentials
   - Use values from your `.env` file

---

## Importing Workflows

### Method 1: Bulk Import via Script

```bash
# Import all workflows
python scripts/workflow_importer.py

# Import specific category
python scripts/workflow_importer.py --category rag-chatbots
```

### Method 2: Manual Import

1. Open n8n dashboard
2. Click "Import from File"
3. Select workflow JSON file from `workflows/` directory
4. Save workflow

### Method 3: Import via URL

If workflows are hosted:
```bash
# In n8n: Import from URL
https://raw.githubusercontent.com/YOUR_USERNAME/Smart-RAG-Chatbot/main/workflows/...
```

---

## Verification

### 1. Test Database Connections

```bash
npm run test:db
```

Expected output:
```
Qdrant: Connected
OpenAI API: Valid
n8n Instance: Running
```

### 2. Validate Workflows

```bash
npm run validate
```

Expected output:
```
25 workflows validated
All JSON structures valid
```

### 3. Test a Simple Workflow

1. Open n8n dashboard
2. Find "Web Search Chatbot" workflow
3. Click "Execute Workflow"
4. Check output - should see successful execution

---

## Troubleshooting

### n8n Won't Start

**Issue**: `n8n: command not found`

**Solution**:
```bash
# Add npm global bin to PATH
export PATH="$PATH:$(npm bin -g)"

# Or reinstall n8n globally
npm install -g n8n
```

### Qdrant Connection Failed

**Issue**: Cannot connect to Qdrant

**Solutions**:
- Check if Qdrant is running: `docker ps` (if using Docker)
- Verify QDRANT_URL in `.env` file
- Try: `http://localhost:6333` or `http://127.0.0.1:6333`
- Check firewall settings

### OpenAI API Key Invalid

**Issue**: 401 Authentication Error

**Solutions**:
- Verify API key is correct
- Check for extra spaces in `.env` file
- Ensure key has necessary permissions
- Generate new key from OpenAI dashboard

### Workflows Import But Don't Execute

**Issue**: Workflows import successfully but fail when executed

**Solutions**:
1. Add credentials in n8n UI:
   - Settings → Credentials
   - Add required credentials
   - Test each credential
2. Update credential IDs in workflows
3. Check webhook URLs if using webhooks

### Python Scripts Not Working

**Issue**: `ModuleNotFoundError`

**Solution**:
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Or install specific missing module
pip install <module_name>
```

---

## Next Steps

After successful installation:

1. **Explore workflows**: Browse the [Workflow Guide](WORKFLOW_GUIDE.md)
2. **Customize**: Modify workflows for your use case
3. **Learn architecture**: Read [Architecture Overview](ARCHITECTURE.md)
4. **Get help**: Check [FAQ](FAQ.md) and [Troubleshooting](TROUBLESHOOTING.md)

---

## Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Project Repository](https://github.com/YOUR_USERNAME/Smart-RAG-Chatbot)

---

**Need help?** Open an issue on [GitHub Issues](https://github.com/YOUR_USERNAME/Smart-RAG-Chatbot/issues)
