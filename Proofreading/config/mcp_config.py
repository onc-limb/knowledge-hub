"""
MCP Client Configuration for Proofreading Agents
"""
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class MCPConfig:
    """Configuration for MCP servers"""
    
    SERVERS = {
        "firecrawl": {
            "command": "npx",
            "args": ["@firecrawl/mcp-server"],
            "env": {
                "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY", "")
            }
        },
        "deepwiki": {
            "command": "npx",
            "args": ["@deepwiki/mcp-server"],
            "env": {
                "DEEPWIKI_API_KEY": os.getenv("DEEPWIKI_API_KEY", "")
            }
        },
        "aws-docs": {
            "command": "npx",
            "args": ["@aws/mcp-server-documentation"],
            "env": {}
        },
        "textlint": {
            "command": "npx",
            "args": ["textlint-mcp-server"],
            "env": {}
        }
    }
    
    @classmethod
    def get_server_config(cls, server_name: str) -> Dict:
        """Get configuration for a specific MCP server"""
        return cls.SERVERS.get(server_name, {})
    
    @classmethod
    def get_all_servers(cls) -> List[str]:
        """Get list of all available MCP servers"""
        return list(cls.SERVERS.keys())