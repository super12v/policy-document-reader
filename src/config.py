"""Configuration management using Pydantic settings."""
from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Server
    server_host: str = Field(default="0.0.0.0", description="Server bind host")
    server_port: int = Field(default=8000, ge=1024, le=65535)
    server_workers: int = Field(default=4, ge=1, le=32)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    # Security
    secret_provider: Literal["vault", "aws", "azure", "gcp"] = "vault"
    secret_endpoint: str = Field(default="http://localhost:8200")
    vault_role: str = "policy-reader"
    vault_token: Optional[str] = None
    
    # Authentication
    auth_enabled: bool = True
    jwt_secret_path: str = "app/jwt-secret"
    jwt_algorithm: str = "RS256"
    jwt_issuer: str = "mcp-policy-reader"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = Field(default=100, ge=1)
    rate_limit_burst: int = Field(default=20, ge=1)
    
    # Metrics
    metrics_enabled: bool = True
    metrics_port: int = Field(default=9090, ge=1024, le=65535)
    metrics_tls_enabled: bool = True
    metrics_cert_path: str = "certs/metrics/exporter.crt"
    metrics_key_path: str = "certs/metrics/exporter.key"
    
    # Document Sources
    smb_enabled: bool = True
    smb_credentials_path: str = "smb/credentials"
    
    git_enabled: bool = True
    git_credentials_path: str = "git/credentials"
    
    sharepoint_enabled: bool = True
    sharepoint_credentials_path: str = "sharepoint/credentials"
    
    s3_enabled: bool = True
    s3_credentials_path: str = "aws/s3-reader"
    
    azure_blob_enabled: bool = True
    azure_credentials_path: str = "azure/blob-reader"
    
    # Document Processing
    max_document_size_mb: int = Field(default=100, ge=1, le=500)
    cache_enabled: bool = True
    cache_ttl_seconds: int = Field(default=3600, ge=60)
    
    # Logging
    log_format: Literal["json", "text"] = "json"
    log_rotation: Literal["daily", "hourly", "size"] = "daily"
    log_retention_days: int = Field(default=365, ge=1)
    audit_log_enabled: bool = True
    pii_redaction_enabled: bool = True


# Global settings instance
settings = Settings()
