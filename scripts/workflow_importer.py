"""
n8n Workflow Importer
Bulk import workflows into n8n instance via API
"""

import json
import requests
import sys
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.panel import Panel
from rich.table import Table
import os

try:
    from dotenv import load_dotenv
except ImportError:
    print("Please install python-dotenv: pip install python-dotenv")
    sys.exit(1)

console = Console()
load_dotenv()


class WorkflowImporter:
    """Import n8n workflows via API"""
    
    def __init__(self):
        self.n8n_host = os.getenv('N8N_HOST', 'localhost')
        self.n8n_port = os.getenv('N8N_PORT', '5678')
        self.n8n_protocol = os.getenv('N8N_PROTOCOL', 'http')
        self.base_url = f"{self.n8n_protocol}://{self.n8n_host}:{self.n8n_port}"
        
        # Basic auth (if configured)
        self.auth = None
        username = os.getenv('N8N_BASIC_AUTH_USER')
        password = os.getenv('N8N_BASIC_AUTH_PASSWORD')
        if username and password:
            self.auth = (username, password)
    
    def test_connection(self) -> bool:
        """Test connection to n8n instance"""
        try:
            response = requests.get(f"{self.base_url}/healthz", timeout=5)
            return response.status_code == 200
        except Exception as e:
            console.print(f"[red]Cannot connect to n8n at {self.base_url}[/red]")
            console.print(f"Error: {e}")
            return False
    
    def import_workflow(self, workflow_path: Path) -> Dict:
        """
        Import a single workflow
        
        Args:
            workflow_path: Path to workflow JSON file
            
        Returns:
            Result dictionary with status and message
        """
        result = {
            'name': workflow_path.stem,
            'status': 'Unknown',
            'message': ''
        }
        
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # Prepare workflow for import
            # Remove id to let n8n assign a new one
            if 'id' in workflow_data:
                del workflow_data['id']
            
            # API endpoint for creating workflows
            url = f"{self.base_url}/api/v1/workflows"
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                url,
                json=workflow_data,
                headers=headers,
                auth=self.auth,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result['status'] = 'Success'
                result['message'] = 'Workflow imported'
                result['id'] = response.json().get('id', '')
            elif response.status_code == 401:
                result['status'] = 'Auth Failed'
                result['message'] = 'Authentication required'
            else:
                result['status'] = 'Failed'
                result['message'] = f'HTTP {response.status_code}'
                
        except json.JSONDecodeError:
            result['status'] = 'Invalid JSON'
            result['message'] = 'Workflow file is not valid JSON'
        except Exception as e:
            result['status'] = 'Error'
            result['message'] = str(e)[:50]
        
        return result
    
    def import_workflows(self, directory: Path, category: Optional[str] = None) -> None:
        """
        Import all workflows from directory
        
        Args:
            directory: Path to workflows directory
            category: Optional category subdirectory to import
        """
        # Find workflow files
        if category:
            search_path = directory / category
        else:
            search_path = directory
        
        if not search_path.exists():
            console.print(f"[red]Directory not found: {search_path}[/red]")
            return
        
        workflow_files = list(search_path.rglob("*.json"))
        
        if not workflow_files:
            console.print(f"[yellow]No workflow files found in {search_path}[/yellow]")
            return
        
        console.print(Panel(
            f"[bold]Found {len(workflow_files)} workflows to import[/bold]\n"
            f"Target: {self.base_url}",
            title="Workflow Importer",
            border_style="cyan"
        ))
        
        # Test connection first
        if not self.test_connection():
            console.print("\n[red][ERROR] Cannot connect to n8n. Please ensure n8n is running.[/red]")
            return
        
        console.print("[green][OK] Connected to n8n[/green]\n")
        
        # Import workflows with progress bar
        results = []
        with Progress() as progress:
            task = progress.add_task("[cyan]Importing workflows...", total=len(workflow_files))
            
            for workflow_file in workflow_files:
                result = self.import_workflow(workflow_file)
                results.append(result)
                progress.update(task, advance=1)
        
        # Display results
        self.display_results(results)
    
    def display_results(self, results: List[Dict]) -> None:
        """Display import results in a table"""
        table = Table(title="\nImport Results", show_header=True, header_style="bold magenta")
        table.add_column("Workflow", style="cyan", width=35)
        table.add_column("Status", justify="center", width=15)
        table.add_column("Message", width=30)
        
        success_count = 0
        failed_count = 0
        
        for result in results:
            name = result['name']
            status = result['status']
            message = result['message']
            
            if status == 'Success':
                status_colored = f"[green][OK] {status}[/green]"
                success_count += 1
            else:
                status_colored = f"[red][ERROR] {status}[/red]"
                failed_count += 1
            
            table.add_row(name, status_colored, message)
        
        console.print(table)
        
        # Summary
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"  [green]Imported:[/green] {success_count}")
        console.print(f"  [red]Failed:[/red] {failed_count}")
        console.print(f"  [cyan]Total:[/cyan] {len(results)}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import n8n workflows via API')
    parser.add_argument('--dir', default='workflows', help='Workflows directory')
    parser.add_argument('--category', help='Import specific category only')
    parser.add_argument('--test-connection', action='store_true', help='Test n8n connection only')
    
    args = parser.parse_args()
    
    importer = WorkflowImporter()
    
    if args.test_connection:
        console.print("Testing connection to n8n...")
        if importer.test_connection():
            console.print(f"[green][OK] Successfully connected to {importer.base_url}[/green]")
        else:
            console.print(f"[red][ERROR] Cannot connect to {importer.base_url}[/red]")
            sys.exit(1)
    else:
        directory = Path(args.dir)
        importer.import_workflows(directory, args.category)


if __name__ == "__main__":
    main()
