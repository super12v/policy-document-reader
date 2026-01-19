"""Git repository reader."""
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse
import tempfile
import git
from src.services.readers.base import BaseReader
from src.utils.logger import logger
from src.utils.errors import SourceConnectionError, NotFoundError


class GitReader(BaseReader):
    """Read documents from Git repositories."""
    
    def __init__(self, temp_dir: Path = Path("/tmp/policy-reader")):
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def read_file(self, path: str, credentials: Dict[str, Any]) -> Path:
        """
        Read file from Git repository.
        
        Path format: git://github.com/org/repo/branch/path/to/file.pdf
        """
        logger.info(f"Reading from Git: {path}")
        
        try:
            # Parse Git URL
            parsed = urlparse(path)
            
            # Extract repo URL and file path
            # Format: git://github.com/org/repo/branch/path/to/file
            path_parts = parsed.path.strip('/').split('/')
            
            # Reconstruct repo URL
            repo_url = f"https://{parsed.hostname}/{path_parts[0]}/{path_parts[1]}"
            branch = path_parts[2] if len(path_parts) > 2 else 'main'
            file_path = '/'.join(path_parts[3:]) if len(path_parts) > 3 else ''
            
            # Clone repository to temp directory
            repo_dir = self.temp_dir / f"repo_{parsed.hostname}_{path_parts[0]}_{path_parts[1]}"
            
            if repo_dir.exists():
                logger.info(f"Using existing clone: {repo_dir}")
                repo = git.Repo(repo_dir)
                repo.remotes.origin.pull()
            else:
                logger.info(f"Cloning repository: {repo_url}")
                
                # Prepare credentials
                if credentials:
                    token = credentials.get('token')
                    if token:
                        repo_url = repo_url.replace('https://', f'https://{token}@')
                
                repo = git.Repo.clone_from(
                    repo_url,
                    repo_dir,
                    branch=branch,
                    depth=1  # Shallow clone
                )
            
            # Get file path
            target_file = repo_dir / file_path
            if not target_file.exists():
                raise NotFoundError(f"File not found in repository: {file_path}")
            
            logger.info(f"Found file: {target_file}")
            return target_file
            
        except Exception as e:
            logger.error(f"Git read failed for {path}: {e}")
            raise SourceConnectionError(f"Git error: {e}")
    
    async def list_files(self, path: str, credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List files in Git repository directory."""
        logger.info(f"Listing Git directory: {path}")
        
        # Clone repo and list files
        # Implementation similar to read_file
        return []
    
    def supports_protocol(self, uri: str) -> bool:
        """Check if protocol is supported."""
        return uri.startswith('git://')
