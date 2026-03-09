"""
n8n Workflow JSON Validator
Validates workflow files for structure, completeness, and best practices
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class WorkflowValidator:
    """Validates n8n workflow JSON files for MySmartRAG-Bot"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}
    
    def validate_json_structure(self, filepath: Path) -> Tuple[bool, Dict]:
        """Validate basic JSON structure"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True, data
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False, None
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False, None
    
    def validate_required_fields(self, data: Dict) -> bool:
        """Check for required workflow fields"""
        required_fields = ['id', 'name', 'nodes']
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            self.errors.append(f"Missing required fields: {', '.join(missing)}")
            return False
        return True
    
    def check_nodes(self, data: Dict) -> Dict:
        """Analyze workflow nodes"""
        nodes = data.get('nodes', [])
        node_stats = {
            'total_nodes': len(nodes),
            'node_types': {},
            'credentials_needed': [],
            'missing_names': []
        }
        
        for node in nodes:
            # Count node types
            node_type = node.get('type', 'unknown')
            node_stats['node_types'][node_type] = node_stats['node_types'].get(node_type, 0) + 1
            
            # Check for credentials
            if 'credentials' in node and node['credentials']:
                for cred_type, cred_data in node['credentials'].items():
                    if cred_data.get('id') or cred_data.get('name'):
                        node_stats['credentials_needed'].append(cred_type)
            
            # Check for unnamed nodes
            if not node.get('name') or node.get('name') == node.get('type'):
                node_stats['missing_names'].append(node.get('id', 'unknown'))
        
        return node_stats
    
    def check_connections(self, data: Dict) -> Dict:
        """Analyze workflow connections"""
        connections = data.get('connections', {})
        return {
            'total_connections': len(connections),
            'has_connections': len(connections) > 0
        }
    
    def validate_metadata(self, data: Dict) -> None:
        """Check for helpful metadata"""
        if not data.get('name') or data['name'].startswith('My workflow'):
            self.warnings.append("Workflow has generic or missing name")
        
        if 'tags' in data and not data['tags']:
            self.warnings.append("No tags defined for categorization")
    
    def validate_workflow(self, filepath: Path) -> Tuple[bool, Dict]:
        """
        Validate a single workflow file
        
        Args:
            filepath: Path to workflow JSON file
            
        Returns:
            Tuple of (is_valid, stats_dict)
        """
        self.errors = []
        self.warnings = []
        
        console.print(f"\n[cyan]Validating:[/cyan] {filepath.name}")
        
        # Check JSON structure
        is_valid_json, data = self.validate_json_structure(filepath)
        if not is_valid_json:
            return False, {}
        
        # Check required fields
        if not self.validate_required_fields(data):
            return False, {}
        
        # Analyze nodes
        node_stats = self.check_nodes(data)
        
        # Analyze connections
        conn_stats = self.check_connections(data)
        
        # Check metadata
        self.validate_metadata(data)
        
        # Compile stats
        stats = {
            'name': data.get('name', 'Unnamed'),
            'id': data.get('id', ''),
            **node_stats,
            **conn_stats,
            'errors': len(self.errors),
            'warnings': len(self.warnings)
        }
        
        # Display results
        if self.errors:
            console.print(f"[red][ERROR] Errors found:[/red]")
            for error in self.errors:
                console.print(f"  - {error}")
        
        if self.warnings:
            console.print(f"[yellow]Warnings:[/yellow]")
            for warning in self.warnings:
                console.print(f"  - {warning}")
        
        if not self.errors:
            console.print(f"[green][OK] Valid workflow[/green]")
            console.print(f"  Nodes: {node_stats['total_nodes']} | Connections: {conn_stats['total_connections']}")
        
        return len(self.errors) == 0, stats
    
    def validate_all_workflows(self, directory: Path) -> None:
        """Validate all workflow files in directory recursively"""
        workflow_files = list(directory.rglob("*.json"))
        
        if not workflow_files:
            console.print("[yellow][WARN] No workflow files found![/yellow]")
            return
        
        console.print(Panel(
            f"[bold]Found {len(workflow_files)} workflow files to validate[/bold]",
            title="Workflow Validator",
            border_style="cyan"
        ))
        
        results = []
        valid_count = 0
        invalid_count = 0
        
        for filepath in workflow_files:
            is_valid, stats = self.validate_workflow(filepath)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
            results.append((filepath, is_valid, stats))
        
        # Summary table
        self.display_summary(results, valid_count, invalid_count)
    
    def display_summary(self, results: List, valid_count: int, invalid_count: int) -> None:
        """Display validation summary table"""
        table = Table(title="\nValidation Summary", show_header=True, header_style="bold magenta")
        table.add_column("Workflow", style="cyan", width=40)
        table.add_column("Status", justify="center", width=10)
        table.add_column("Nodes", justify="right", width=8)
        table.add_column("Connections", justify="right", width=12)
        table.add_column("Issues", justify="center", width=10)
        
        for filepath, is_valid, stats in results:
            status = "[green][OK] Valid[/green]" if is_valid else "[red][ERROR] Invalid[/red]"
            nodes = str(stats.get('total_nodes', 0))
            conns = str(stats.get('total_connections', 0))
            issues = f"{stats.get('errors', 0)}E / {stats.get('warnings', 0)}W"
            
            table.add_row(filepath.stem, status, nodes, conns, issues)
        
        console.print(table)
        
        # Final summary
        console.print(f"\n[bold]Results:[/bold]")
        console.print(f"  [green]Valid:[/green] {valid_count}")
        console.print(f"  [red]Invalid:[/red] {invalid_count}")
        console.print(f"  [cyan]Total:[/cyan] {valid_count + invalid_count}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate n8n workflow JSON files')
    parser.add_argument('--path', default='workflows', help='Path to workflows directory')
    parser.add_argument('--file', help='Validate a single file')
    parser.add_argument('--check-all', action='store_true', help='Check all workflows recursively')
    
    args = parser.parse_args()
    
    validator = WorkflowValidator()
    
    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            console.print(f"[red]Error: File not found: {filepath}[/red]")
            sys.exit(1)
        is_valid, _ = validator.validate_workflow(filepath)
        sys.exit(0 if is_valid else 1)
    
    elif args.check_all:
        directory = Path(args.path)
        if not directory.exists():
            console.print(f"[red]Error: Directory not found: {directory}[/red]")
            sys.exit(1)
        validator.validate_all_workflows(directory)
    
    else:
        console.print("[yellow]Please specify --file or --check-all[/yellow]")
        parser.print_help()


if __name__ == "__main__":
    main()
