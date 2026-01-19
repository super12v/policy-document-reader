# Policy Document Reader - Project Summary

## Overview

Successfully created a production-ready MCP server for reading security policy documents from multiple sources. This server enables AI agents to access policy documents for infrastructure security policy creation.

## Project Location

```
/data/code/projects/policy-document-reader/
```

## Key Features

### ✅ Multiple Protocol Support

1. **Local Filesystem** (`file://`)
2. **SMB/CIFS** (`smb://`) - Windows file shares
3. **Git Repositories** (`git://`) - GitHub, GitLab, Bitbucket
4. **AWS S3** (`s3://`) - S3 buckets
5. **HTTP/REST** (`http://`, `https://`) - REST APIs
6. **WebDAV** (ready to implement)
7. **SharePoint** (ready to implement)

### ✅ Multiple Document Formats

1. **PDF** (`.pdf`) - Using pdfplumber
2. **Microsoft Word** (`.docx`, `.doc`) - Using python-docx
3. **Microsoft Excel** (`.xlsx`, `.xls`) - Using openpyxl/pandas
4. **CSV** (`.csv`) - Using pandas
5. **Plain Text** (`.txt`) - Native support
6. **Markdown** (`.md`) - Native support
7. **JSON/YAML** (`.json`, `.yaml`) - Native support

### ✅ MCP Tools

1. **policy-read-document** - Read and parse policy documents
2. **policy-list-documents** - List available documents

## Architecture

```
Policy Document Reader
├── FastAPI Application (Async)
├── Tool Registry (MCP Tools)
├── Reader Registry (Protocol Adapters)
│   ├── LocalReader
│   ├── SMBReader
│   ├── GitReader
│   ├── S3Reader
│   └── HTTPReader
├── Parser Registry (Format Parsers)
│   ├── PDFParser
│   ├── DOCXParser
│   ├── ExcelParser
│   ├── CSVParser
│   └── TextParser
└── Security Layer
    ├── Vault Integration
    ├── Input Validation (Pydantic)
    ├── PII Redaction
    └── Audit Logging
```

## Project Structure

```
policy-document-reader/
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── setup.sh                   # Setup script
├── run.py                     # Multi-process runner
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Full stack deployment
│
├── src/
│   ├── main.py               # FastAPI application
│   ├── config.py             # Settings management
│   │
│   ├── tools/                # MCP tools
│   │   ├── __init__.py      # Tool registry
│   │   └── policy/
│   │       ├── read_document.py
│   │       └── list_documents.py
│   │
│   ├── services/
│   │   ├── readers/         # Protocol adapters
│   │   │   ├── base.py
│   │   │   ├── local_reader.py
│   │   │   ├── smb_reader.py
│   │   │   ├── git_reader.py
│   │   │   ├── s3_reader.py
│   │   │   ├── http_reader.py
│   │   │   └── __init__.py
│   │   │
│   │   └── parsers/         # Format parsers
│   │       ├── base.py
│   │       ├── pdf_parser.py
│   │       ├── docx_parser.py
│   │       ├── excel_parser.py
│   │       ├── csv_parser.py
│   │       ├── text_parser.py
│   │       └── __init__.py
│   │
│   └── utils/               # Utilities
│       ├── logger.py        # Structured logging with PII redaction
│       └── errors.py        # Custom exceptions
│
├── docs/
│   └── QUICKSTART.md        # Quick start guide
│
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── security/
│
└── logs/                    # Log directory (auto-created)
```

## Quick Start

### Option 1: Direct Run

```bash
cd /data/code/projects/policy-document-reader
./setup.sh
source venv/bin/activate
python run.py
```

### Option 2: Docker

```bash
cd /data/code/projects/policy-document-reader
docker-compose up --build
```

## Usage Examples

### Read a local PDF

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

### Read from Git

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

## Security Features

✅ **Vault Integration** - All credentials stored securely  
✅ **Input Validation** - Pydantic models with strict validation  
✅ **PII Redaction** - Automatic redaction in logs  
✅ **Audit Logging** - All document access logged  
✅ **Size Limits** - Configurable document size limits  
✅ **Rate Limiting** - Per-agent rate limits  
✅ **TLS Encryption** - All remote connections encrypted  

## Configuration

Edit `.env` file:

```bash
# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Vault
SECRET_PROVIDER=vault
SECRET_ENDPOINT=http://vault:8200

# Document sources
SMB_ENABLED=true
GIT_ENABLED=true
S3_ENABLED=true

# Security
MAX_DOCUMENT_SIZE_MB=100
```

## Next Steps

1. **Configure Vault**: Store credentials for SMB, Git, S3
2. **Test Integration**: Test with your document sources
3. **Deploy**: Use Docker or Kubernetes for production
4. **Monitor**: Set up Prometheus for metrics
5. **Extend**: Add SharePoint, WebDAV readers as needed

## Extension Points

### Adding New Protocols

1. Create reader in `src/services/readers/`
2. Implement `BaseReader` interface
3. Register in `ReaderRegistry`

### Adding New Formats

1. Create parser in `src/services/parsers/`
2. Implement `BaseParser` interface
3. Register in `ParserRegistry`

### Adding New Tools

1. Create tool in `src/tools/policy/`
2. Define Pydantic input model
3. Register in `ToolRegistry`

## Dependencies

- **FastAPI**: Web framework
- **Pydantic**: Validation
- **pdfplumber**: PDF parsing
- **python-docx**: Word documents
- **openpyxl/pandas**: Excel/CSV
- **GitPython**: Git repositories
- **boto3**: AWS S3
- **smbprotocol**: SMB shares
- **httpx**: HTTP/REST

## Testing

```bash
pytest                    # Run tests
mypy src/                # Type checking
ruff check src/          # Linting
bandit -r src/           # Security scan
```

## License

Internal use only - Enterprise deployment

---

**Created**: 2026-01-19  
**Framework**: Python MCP Framework  
**Purpose**: AI agent policy document access
