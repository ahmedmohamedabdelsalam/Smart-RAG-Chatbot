"""
Workflow Backup and Restore Utility
Backup workflows with timestamps and restore from backups
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from rich.panel import Panel

console = Console()


class WorkflowBackup:
    """Manage workflow backups and restores"""
    
    def __init__(self, workflows_dir: str = "workflows", backup_dir: str = "backups"):
        self.workflows_dir = Path(workflows_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, description: str = "") -> Optional[Path]:
        """
        Create a timestamped backup of all workflows
        
        Args:
            description: Optional description for the backup
            
        Returns:
            Path to backup directory or None if failed
        """
        if not self.workflows_dir.exists():
            console.print(f"[red]Error: Workflows directory not found: {self.workflows_dir}[/red]")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        if description:
            # Sanitize description for filename
            desc_clean = "".join(c if c.isalnum() else "_" for c in description)[:30]
            backup_name = f"backup_{timestamp}_{desc_clean}"
        
        backup_path = self.backup_dir / backup_name
        
        try:
            console.print(f"\n[cyan]Creating backup: {backup_name}[/cyan]")
            
            # Count workflows
            workflow_files = list(self.workflows_dir.rglob("*.json"))
            console.print(f"Found {len(workflow_files)} workflow files")
            
            # Copy entire workflows directory
            shutil.copytree(self.workflows_dir, backup_path)
            
            # Create metadata file
            metadata = {
                'timestamp': timestamp,
                'description': description,
                'workflow_count': len(workflow_files),
                'source_directory': str(self.workflows_dir.absolute())
            }
            
            metadata_file = backup_path / "backup_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            console.print(f"[green][OK] Backup created successfully: {backup_path}[/green]")
            console.print(f"  Backed up {len(workflow_files)} workflows")
            
            return backup_path
            
        except Exception as e:
            console.print(f"[red][ERROR] Backup failed: {e}[/red]")
            # Clean up partial backup
            if backup_path.exists():
                shutil.rmtree(backup_path)
            return None
    
    def list_backups(self) -> List[dict]:
        """List all available backups with metadata"""
        if not self.backup_dir.exists():
            return []
        
        backups = []
        for backup_path in sorted(self.backup_dir.glob("backup_*"), reverse=True):
            if backup_path.is_dir():
                metadata_file = backup_path / "backup_metadata.json"
                
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    metadata['path'] = backup_path
                    backups.append(metadata)
                else:
                    # Backup without metadata
                    backups.append({
                        'timestamp': backup_path.name.replace('backup_', ''),
                        'description': 'No description',
                        'workflow_count': len(list(backup_path.rglob("*.json"))),
                        'path': backup_path
                    })
        
        return backups
    
    def display_backups(self) -> None:
        """Display available backups in a table"""
        backups = self.list_backups()
        
        if not backups:
            console.print("[yellow]No backups found.[/yellow]")
            return
        
        table = Table(title="Available Backups", show_header=True, header_style="bold magenta")
        table.add_column("#", justify="right", style="cyan", width=4)
        table.add_column("Timestamp", style="green", width=20)
        table.add_column("Description", width=30)
        table.add_column("Workflows", justify="right", width=12)
        table.add_column("Path", style="dim", width=40)
        
        for idx, backup in enumerate(backups, 1):
            table.add_row(
                str(idx),
                backup['timestamp'],
                backup.get('description', 'No description')[:30],
                str(backup['workflow_count']),
                str(backup['path'].name)
            )
        
        console.print(table)
    
    def restore_backup(self, backup_path: Path, target_dir: Optional[Path] = None) -> bool:
        """
        Restore workflows from backup
        
        Args:
            backup_path: Path to backup directory
            target_dir: Target directory to restore to (default: workflows_dir)
            
        Returns:
            True if successful, False otherwise
        """
        if not backup_path.exists():
            console.print(f"[red]Error: Backup not found: {backup_path}[/red]")
            return False
        
        target = target_dir if target_dir else self.workflows_dir
        
        console.print(f"\n[yellow][WARNING] Warning: This will replace all workflows in {target}[/yellow]")
        if not Confirm.ask("Continue with restore?", default=False):
            console.print("[cyan]Restore cancelled.[/cyan]")
            return False
        
        try:
            # Create backup of current state first
            console.print("\n[cyan]Creating safety backup of current state...[/cyan]")
            self.create_backup("pre_restore_safety_backup")
            
            # Remove current workflows
            if target.exists():
                console.print(f"Removing current workflows from {target}")
                shutil.rmtree(target)
            
            # Copy backup to target
            console.print(f"Restoring backup from {backup_path.name}")
            shutil.copytree(backup_path, target)
            
            # Remove metadata file from restored directory
            metadata_file = target / "backup_metadata.json"
            if metadata_file.exists():
                metadata_file.unlink()
            
            workflow_count = len(list(target.rglob("*.json")))
            console.print(f"[green][OK] Restore completed successfully![/green]")
            console.print(f"  Restored {workflow_count} workflows")
            
            return True
            
        except Exception as e:
            console.print(f"[red][ERROR] Restore failed: {e}[/red]")
            return False
    
    def delete_backup(self, backup_path: Path) -> bool:
        """Delete a backup"""
        if not backup_path.exists():
            console.print(f"[red]Backup not found: {backup_path}[/red]")
            return False
        
        try:
            shutil.rmtree(backup_path)
            console.print(f"[green][OK] Backup deleted: {backup_path.name}[/green]")
            return True
        except Exception as e:
            console.print(f"[red][ERROR] Failed to delete backup: {e}[/red]")
            return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup and restore n8n workflows')
    parser.add_argument('--workflows-dir', default='workflows', help='Workflows directory')
    parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create backup
    backup_parser = subparsers.add_parser('create', help='Create a new backup')
    backup_parser.add_argument('--description', '-d', help='Backup description')
    
    # List backups
    subparsers.add_parser('list', help='List available backups')
    
    # Restore backup
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup_name', help='Name of backup to restore')
    restore_parser.add_argument('--target', help='Target directory (default: workflows)')
    
    # Delete backup
    delete_parser = subparsers.add_parser('delete', help='Delete a backup')
    delete_parser.add_argument('backup_name', help='Name of backup to delete')
    
    args = parser.parse_args()
    
    backup_manager = WorkflowBackup(args.workflows_dir, args.backup_dir)
    
    if args.command == 'create':
        backup_manager.create_backup(args.description or "")
    
    elif args.command == 'list':
        backup_manager.display_backups()
    
    elif args.command == 'restore':
        backup_path = Path(args.backup_dir) / args.backup_name
        target = Path(args.target) if args.target else None
        backup_manager.restore_backup(backup_path, target)
    
    elif args.command == 'delete':
        backup_path = Path(args.backup_dir) / args.backup_name
        backup_manager.delete_backup(backup_path)
    
    else:
        console.print(Panel(
            "[bold]Workflow Backup Manager[/bold]\n\n"
            "Commands:\n"
            "  create   - Create a new backup\n"
            "  list     - List available backups\n"
            "  restore  - Restore from backup\n"
            "  delete   - Delete a backup\n\n"
            "Example:\n"
            "  python backup_workflows.py create --description 'Before major changes'\n"
            "  python backup_workflows.py list\n"
            "  python backup_workflows.py restore backup_20260208_120000",
            border_style="cyan"
        ))


if __name__ == "__main__":
    main()
