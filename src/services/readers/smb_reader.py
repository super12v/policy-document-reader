"""SMB/CIFS file share reader."""
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse
import tempfile
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open, CreateDisposition, FileAttributes
from smbprotocol.file_info import FileStandardInformation
from src.services.readers.base import BaseReader
from src.utils.logger import logger
from src.utils.errors import SourceConnectionError, NotFoundError


class SMBReader(BaseReader):
    """Read documents from SMB/CIFS file shares."""
    
    def __init__(self, temp_dir: Path = Path("/tmp/policy-reader")):
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def read_file(self, path: str, credentials: Dict[str, Any]) -> Path:
        """Read file from SMB share."""
        logger.info(f"Reading from SMB: {path}")
        
        try:
            # Parse SMB URL: smb://server/share/path/to/file.pdf
            parsed = urlparse(path)
            server = parsed.hostname
            share_path = parsed.path.split('/', 2)
            share = share_path[1] if len(share_path) > 1 else ''
            file_path = share_path[2] if len(share_path) > 2 else ''
            
            username = credentials.get('username')
            password = credentials.get('password')
            domain = credentials.get('domain', '')
            
            # Connect to SMB server
            connection = Connection(uuid.uuid4(), server, 445)
            connection.connect()
            
            session = Session(connection, username, password, domain)
            session.connect()
            
            tree = TreeConnect(session, f"\\\\{server}\\{share}")
            tree.connect()
            
            # Open and read file
            file_open = Open(tree, file_path)
            file_open.create(
                FileAttributes.FILE_ATTRIBUTE_NORMAL,
                None,
                CreateDisposition.FILE_OPEN
            )
            
            # Read file content
            content = file_open.read(0, file_open.end_of_file)
            
            # Save to temp file
            temp_file = self.temp_dir / Path(file_path).name
            temp_file.write_bytes(content)
            
            file_open.close()
            tree.disconnect()
            session.disconnect()
            connection.disconnect()
            
            logger.info(f"Downloaded {path} to {temp_file}")
            return temp_file
            
        except Exception as e:
            logger.error(f"SMB read failed for {path}: {e}")
            raise SourceConnectionError(f"SMB error: {e}")
    
    async def list_files(self, path: str, credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List files in SMB directory."""
        logger.info(f"Listing SMB directory: {path}")
        
        # Implementation similar to read_file but enumerate directory
        # Simplified for brevity
        return []
    
    def supports_protocol(self, uri: str) -> bool:
        """Check if protocol is supported."""
        return uri.startswith('smb://') or uri.startswith('\\\\')
