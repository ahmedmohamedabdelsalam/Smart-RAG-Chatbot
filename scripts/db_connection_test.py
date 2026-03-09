"""
Database Connection Tester
Tests connections to vector databases and external APIs
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

try:
    from dotenv import load_dotenv
except ImportError:
    print("Please install python-dotenv: pip install python-dotenv")
    sys.exit(1)

console = Console()


class ConnectionTester:
    """Test connections to external services"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)
        self.load_env()
        self.results = {}
    
    def load_env(self) -> None:
        """Load environment variables"""
        if self.env_file.exists():
            load_dotenv(self.env_file)
            console.print(f"[green][OK] Loaded environment from {self.env_file}[/green]\n")
        else:
            console.print(f"[yellow][WARNING] No .env file found at {self.env_file}[/yellow]\n")
    
    def test_qdrant_connection(self) -> Dict:
        """Test Qdrant vector database connection"""
        result = {
            'service': 'Qdrant Vector Database',
            'status': 'Unknown',
            'message': ''
        }
        
        qdrant_url = os.getenv('QDRANT_URL')
        if not qdrant_url:
            result['status'] = 'Not Configured'
            result['message'] = 'QDRANT_URL not set in environment'
            return result
        
        try:
            from qdrant_client import QdrantClient
            
            api_key = os.getenv('QDRANT_API_KEY')
            client = QdrantClient(
                url=qdrant_url,
                api_key=api_key if api_key else None
            )
            
            # Try to get collections
            collections = client.get_collections()
            result['status'] = 'Connected'
            result['message'] = f'Found {len(collections.collections)} collection(s)'
            
        except ImportError:
            result['status'] = 'Library Missing'
            result['message'] = 'Install: pip install qdrant-client'
        except Exception as e:
            result['status'] = 'Failed'
            result['message'] = str(e)[:100]
        
        return result
    
    def test_openai_connection(self) -> Dict:
        """Test OpenAI API connection"""
        result = {
            'service': 'OpenAI API',
            'status': 'Unknown',
            'message': ''
        }
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key.startswith('your_'):
            result['status'] = 'Not Configured'
            result['message'] = 'OPENAI_API_KEY not set in environment'
            return result
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            # Test with models list (lightweight operation)
            models = client.models.list()
            result['status'] = 'Connected'
            result['message'] = f'API key valid, {len(list(models))} models available'
            
        except ImportError:
            result['status'] = 'Library Missing'
            result['message'] = 'Install: pip install openai'
        except Exception as e:
            result['status'] = 'Failed'
            error_msg = str(e)[:100]
            if 'authentication' in error_msg.lower() or 'api_key' in error_msg.lower():
                result['message'] = 'Invalid API key'
            else:
                result['message'] = error_msg
        
        return result
    
    def test_gemini_connection(self) -> Dict:
        """Test Google Gemini API connection"""
        result = {
            'service': 'Google Gemini API',
            'status': 'Unknown',
            'message': ''
        }
        
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if not api_key or api_key.startswith('your_'):
            result['status'] = 'Not Configured'
            result['message'] = 'GOOGLE_GEMINI_API_KEY not set'
            return result
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=api_key)
            # List models to verify connection
            models = genai.list_models()
            result['status'] = 'Connected'
            result['message'] = f'API key valid, {len(list(models))} models available'
            
        except ImportError:
            result['status'] = 'Library Missing'
            result['message'] = 'Install: pip install google-generativeai'
        except Exception as e:
            result['status'] = 'Failed'
            result['message'] = str(e)[:100]
        
        return result
    
    def test_n8n_connection(self) -> Dict:
        """Test n8n instance connection"""
        result = {
            'service': 'n8n Instance',
            'status': 'Unknown',
            'message': ''
        }
        
        host = os.getenv('N8N_HOST', 'localhost')
        port = os.getenv('N8N_PORT', '5678')
        protocol = os.getenv('N8N_PROTOCOL', 'http')
        
        try:
            import requests
            
            url = f"{protocol}://{host}:{port}/healthz"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                result['status'] = 'Connected'
                result['message'] = f'n8n running at {protocol}://{host}:{port}'
            else:
                result['status'] = 'Failed'
                result['message'] = f'HTTP {response.status_code}'
                
        except ImportError:
            result['status'] = 'Library Missing'
            result['message'] = 'Install: pip install requests'
        except Exception as e:
            result['status'] = 'Failed'
            result['message'] = f'Cannot reach {protocol}://{host}:{port}'
        
        return result
    
    def test_all_connections(self) -> None:
        """Test all configured connections"""
        console.print(Panel(
            "[bold]Testing Connections to External Services[/bold]",
            border_style="cyan"
        ))
        
        tests = [
            self.test_n8n_connection,
            self.test_qdrant_connection,
            self.test_openai_connection,
            self.test_gemini_connection
        ]
        
        results = []
        for test_func in tests:
            console.print(f"Testing {test_func.__name__.replace('test_', '').replace('_connection', '')}...")
            result = test_func()
            results.append(result)
            self.results[result['service']] = result
        
        self.display_results(results)
    
    def display_results(self, results: list) -> None:
        """Display test results in a table"""
        table = Table(title="\nConnection Test Results", show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan", width=25)
        table.add_column("Status", justify="center", width=15)
        table.add_column("Message", width=50)
        
        for result in results:
            service = result['service']
            status = result['status']
            message = result['message']
            
            # Color code status
            if status == 'Connected':
                status_colored = f"[green]+ {status}[/green]"
            elif status == 'Not Configured':
                status_colored = f"[yellow]o {status}[/yellow]"
            elif status == 'Library Missing':
                status_colored = f"[cyan]* {status}[/cyan]"
            else:
                status_colored = f"[red][ERROR] {status}[/red]"
            
            table.add_row(service, status_colored, message)
        
        console.print(table)
        
        # Summary
        connected = sum(1 for r in results if r['status'] == 'Connected')
        total = len(results)
        console.print(f"\n[bold]Summary:[/bold] {connected}/{total} services connected")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test connections to external services')
    parser.add_argument('--env', default='.env', help='Path to .env file')
    parser.add_argument('--service', choices=['qdrant', 'openai', 'gemini', 'n8n'],
                        help='Test specific service only')
    
    args = parser.parse_args()
    
    tester = ConnectionTester(args.env)
    
    if args.service:
        test_methods = {
            'qdrant': tester.test_qdrant_connection,
            'openai': tester.test_openai_connection,
            'gemini': tester.test_gemini_connection,
            'n8n': tester.test_n8n_connection
        }
        result = test_methods[args.service]()
        console.print(f"\n{result['service']}: {result['status']} - {result['message']}")
    else:
        tester.test_all_connections()


if __name__ == "__main__":
    main()
