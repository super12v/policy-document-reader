# Policy Document Reader - MCP Server

An enterprise-grade MCP server for reading and parsing security policy documents from multiple sources for AI agent consumption.

## Purpose

This MCP server enables AI agents to access policy documents from various sources (file shares, SharePoint, Git, local filesystem) and formats (PDF, DOCX, XLSX, CSV, TXT) to help create infrastructure security policies.

## Supported Sources

- **Local Filesystem**: Direct file access
- **SMB/CIFS**: Windows file shares
- **WebDAV**: Web-based file access
- **Git**: GitHub, GitLab, Bitbucket repositories
- **SharePoint**: Microsoft SharePoint document libraries
- **REST APIs**: Generic REST endpoints
- **S3**: AWS S3 buckets
- **Azure Blob**: Azure Storage

## Supported Formats

- **PDF**: Portable Document Format
- **DOCX**: Microsoft Word documents
- **XLSX**: Microsoft Excel spreadsheets
- **CSV**: Comma-separated values
- **TXT**: Plain text files
- **Markdown**: .md files
- **JSON/YAML**: Structured policy files

## MCP Tools

### `policy-read-document`
Read a single policy document from any supported source.

### `policy-list-documents`
List available documents in a source location.

### `policy-search-content`
Search for specific content across policy documents.

### `policy-extract-metadata`
Extract metadata from policy documents (author, date, version, etc.).

## Security Features

- ✅ Vault integration for credential management
- ✅ Automatic PII redaction in logs
- ✅ Input validation with Pydantic
- ✅ Rate limiting per agent
- ✅ Audit logging for all document access
- ✅ TLS encryption for all remote connections
- ✅ Least privilege access model

## Quick Start

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run the server
python run.py
```

## Architecture

Built on the Python MCP Framework with:
- **FastAPI**: Async web framework
- **Pydantic**: Schema validation
- **Multiple protocol adapters**: Pluggable source readers
- **Format parsers**: Extensible document parsers
- **Prometheus metrics**: Observability
- **Structured logging**: Automatic PII redaction

## Usage Example

```python
# Agent requests a policy document via MCP
{
  "tool": "policy-read-document",
  "arguments": {
    "source": "smb://fileserver/policies/security-policy-2024.pdf",
    "credentials_path": "smb/fileserver",
    "format": "pdf"
  }
}

# Response
{
  "content": "... parsed document text ...",
  "metadata": {
    "title": "Security Policy 2024",
    "author": "Security Team",
    "pages": 42,
    "created": "2024-01-15"
  }
}
```

## Development

```bash
# Run tests
pytest

# Type checking
mypy src/

# Linting
ruff check src/

# Format
black src/
```

## License

Internal use only - Enterprise deployment
