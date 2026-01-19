# Policy Document Reader - MCP Server

## Quick Start Guide

### 1. Setup

```bash
# Run setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configuration

Edit `.env` file:
```bash
# Vault configuration for credentials
SECRET_PROVIDER=vault
SECRET_ENDPOINT=http://vault:8200

# Enable document sources
SMB_ENABLED=true
GIT_ENABLED=true
S3_ENABLED=true
```

### 3. Run

```bash
# Development
python run.py

# Or with Docker
docker-compose up --build
```

## Usage Examples

### Read a PDF from local filesystem

```bash
curl -X POST http://localhost:8000/api/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "policy-read-document",
    "arguments": {
      "source": "file:///path/to/security-policy.pdf"
    }
  }'
```

### Read from SMB share

```bash
curl -X POST http://localhost:8000/api/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "policy-read-document",
    "arguments": {
      "source": "smb://fileserver/policies/network-policy.docx",
      "credentials_path": "smb/fileserver"
    }
  }'
```

### Read from Git repository

```bash
curl -X POST http://localhost:8000/api/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "policy-read-document",
    "arguments": {
      "source": "git://github.com/org/policies/main/security/firewall.md",
      "credentials_path": "git/github"
    }
  }'
```

### Read from S3

```bash
curl -X POST http://localhost:8000/api/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "policy-read-document",
    "arguments": {
      "source": "s3://policy-bucket/compliance/iso27001.xlsx",
      "credentials_path": "aws/s3-reader"
    }
  }'
```

### List documents

```bash
curl -X POST http://localhost:8000/api/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "policy-list-documents",
    "arguments": {
      "source": "s3://policy-bucket/security/",
      "pattern": "*.pdf"
    }
  }'
```

## Supported Protocols

- `file://` - Local filesystem
- `smb://` - SMB/CIFS file shares
- `git://` - Git repositories (GitHub, GitLab, Bitbucket)
- `s3://` - AWS S3 buckets
- `http://` / `https://` - HTTP/REST APIs
- `webdav://` - WebDAV servers (future)
- `sharepoint://` - SharePoint (future)

## Supported Formats

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Microsoft Excel (`.xlsx`, `.xls`)
- CSV (`.csv`)
- Plain Text (`.txt`)
- Markdown (`.md`)
- JSON/YAML (`.json`, `.yaml`)

## Security

All credentials are stored in HashiCorp Vault:

```bash
# Store SMB credentials
vault kv put smb/fileserver username=user password=pass domain=DOMAIN

# Store Git token
vault kv put git/github token=ghp_xxxxx

# Store S3 credentials
vault kv put aws/s3-reader access_key_id=xxx secret_access_key=yyy
```

## Architecture

```
┌──────────────┐
│  AI Agent    │
└──────┬───────┘
       │ MCP Protocol
       ▼
┌──────────────────────┐
│  Policy Reader API   │
├──────────────────────┤
│  Tool Registry       │
│  - read-document     │
│  - list-documents    │
└──────┬───────────────┘
       │
       ├─► Reader Registry
       │   ├─► Local Reader
       │   ├─► SMB Reader
       │   ├─► Git Reader
       │   ├─► S3 Reader
       │   └─► HTTP Reader
       │
       └─► Parser Registry
           ├─► PDF Parser
           ├─► DOCX Parser
           ├─► Excel Parser
           ├─► CSV Parser
           └─► Text Parser
```

## Development

```bash
# Run tests
pytest

# Type checking
mypy src/

# Linting
ruff check src/
black src/

# Security scan
bandit -r src/
```

## Deployment

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: policy-reader
spec:
  replicas: 3
  selector:
    matchLabels:
      app: policy-reader
  template:
    metadata:
      labels:
        app: policy-reader
    spec:
      containers:
      - name: policy-reader
        image: policy-reader:latest
        ports:
        - containerPort: 8000
        - containerPort: 9090
        env:
        - name: VAULT_ADDR
          value: "http://vault:8200"
```

## Monitoring

- **Metrics**: http://localhost:9090/metrics (Prometheus format)
- **Health**: http://localhost:8000/health
- **Logs**: `logs/` directory (JSON format)

## License

Internal use only - Enterprise deployment
