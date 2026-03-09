"""
Interactive Setup Wizard for Smart-RAG-Chatbot
Guides users through environment configuration and initial setup
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress
import re

try:
    from dotenv import load_dotenv, set_key
except ImportError:
    print("Please install python-dotenv: pip install python-dotenv")
    sys.exit(1)

console = Console()


class SetupWizard:
    """Interactive setup wizard for project configuration"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.env_file = self.base_dir / ".env"
        self.env_example = self.base_dir / ".env.example"
        self.config = {}
    
    def welcome(self) -> None:
        """Display welcome message"""
        console.print(Panel.fit(
            "[bold cyan]MySmartRAG-Bot Setup Wizard[/bold cyan]\n\n"
            "This utility will guide you through the initial configuration.\n"
            "Press Enter to use default values or skip optional fields.",
            border_style="cyan"
        ))
    
    def check_existing_env(self) -> bool:
        """Check if .env file already exists"""
        if self.env_file.exists():
            console.print("\n[yellow][WARNING] .env file already exists![/yellow]")
            overwrite = Confirm.ask("Do you want to overwrite it?", default=False)
            if not overwrite:
                console.print("[cyan]Setup cancelled. Existing configuration preserved.[/cyan]")
                return False
        return True
    
    def validate_api_key(self, key: str) -> bool:
        """Basic API key validation"""
        if not key or key.startswith("your_") or key == "":
            return False
        return len(key) > 10
    
    def collect_api_keys(self) -> None:
        """Collect API keys from user"""
        console.print("\n[bold]📦 API Configuration[/bold]")
        console.print("Configure your API keys and credentials.\n")
        
        # OpenAI
        openai_key = Prompt.ask(
            "OpenAI API Key",
            password=True,
            default=""
        )
        self.config['OPENAI_API_KEY'] = openai_key if openai_key else "your_openai_api_key_here"
        
        # Gemini
        gemini_key = Prompt.ask(
            "Google Gemini API Key (optional)",
            password=True,
            default=""
        )
        self.config['GOOGLE_GEMINI_API_KEY'] = gemini_key if gemini_key else "your_gemini_api_key_here"
        
        # Qdrant
        use_qdrant = Confirm.ask("\nWill you be using Qdrant vector database?", default=True)
        if use_qdrant:
            qdrant_url = Prompt.ask(
                "Qdrant URL",
                default="http://localhost:6333"
            )
            qdrant_key = Prompt.ask(
                "Qdrant API Key (optional for local)",
                password=True,
                default=""
            )
            self.config['QDRANT_URL'] = qdrant_url
            self.config['QDRANT_API_KEY'] = qdrant_key if qdrant_key else ""
            self.config['QDRANT_COLLECTION_NAME'] = Prompt.ask(
                "Qdrant Collection Name",
                default="my_documents"
            )
        
        # n8n Configuration
        console.print("\n[bold]🔧 n8n Configuration[/bold]")
        n8n_host = Prompt.ask("n8n Host", default="localhost")
        n8n_port = Prompt.ask("n8n Port", default="5678")
        self.config['N8N_HOST'] = n8n_host
        self.config['N8N_PORT'] = n8n_port
        self.config['N8N_PROTOCOL'] = "http"
        
        # Optional integrations
        console.print("\n[bold]🔌 Optional Integrations[/bold]")
        console.print("Press Enter to skip any optional integration.\n")
        
        # Telegram
        if Confirm.ask("Configure Telegram bot?", default=False):
            tg_token = Prompt.ask("Telegram Bot Token", password=True)
            tg_chat = Prompt.ask("Telegram Chat ID")
            self.config['TELEGRAM_BOT_TOKEN'] = tg_token
            self.config['TELEGRAM_CHAT_ID'] = tg_chat
        
        # Google Drive
        if Confirm.ask("Configure Google Drive integration?", default=False):
            gd_client = Prompt.ask("Google Drive Client ID")
            gd_secret = Prompt.ask("Google Drive Client Secret", password=True)
            self.config['GOOGLE_DRIVE_CLIENT_ID'] = gd_client
            self.config['GOOGLE_DRIVE_CLIENT_SECRET'] = gd_secret
    
    def create_env_file(self) -> None:
        """Create .env file with collected configuration"""
        console.print("\n[bold]💾 Creating .env file...[/bold]")
        
        # Load template from .env.example
        env_content = []
        
        if self.env_example.exists():
            with open(self.env_example, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key = line.split('=')[0]
                        if key in self.config:
                            env_content.append(f"{key}={self.config[key]}")
                        else:
                            env_content.append(line)
                    else:
                        env_content.append(line)
        else:
            # Create from scratch if template doesn't exist
            for key, value in self.config.items():
                env_content.append(f"{key}={value}")
        
        # Write to .env file
        with open(self.env_file, 'w') as f:
            f.write('\n'.join(env_content))
        
        console.print(f"[green][OK] .env file created successfully![/green]")
    
    def test_connections(self) -> None:
        """Test API connections"""
        if not Confirm.ask("\nWould you like to test your API connections?", default=True):
            return
        
        console.print("\n[bold]🔍 Testing Connections...[/bold]\n")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Testing APIs...", total=3)
            
            # Test OpenAI
            if self.config.get('OPENAI_API_KEY') and self.validate_api_key(self.config['OPENAI_API_KEY']):
                try:
                    # Basic validation (not actual API call to avoid costs)
                    progress.console.print("[green][OK] OpenAI API key format valid[/green]")
                except Exception as e:
                    progress.console.print(f"[red][ERROR] OpenAI connection failed: {e}[/red]")
            progress.update(task, advance=1)
            
            # Test Gemini
            if self.config.get('GOOGLE_GEMINI_API_KEY') and self.validate_api_key(self.config['GOOGLE_GEMINI_API_KEY']):
                progress.console.print("[green][OK] Gemini API key format valid[/green]")
            progress.update(task, advance=1)
            
            # Test Qdrant
            if self.config.get('QDRANT_URL'):
                progress.console.print(f"[green][OK] Qdrant configured: {self.config['QDRANT_URL']}[/green]")
            progress.update(task, advance=1)
    
    def display_next_steps(self) -> None:
        """Display next steps for the user"""
        console.print(Panel(
            "[bold green][OK] Setup Complete![/bold green]\n\n"
            "[bold]Next Steps:[/bold]\n"
            "1. Review your .env file and update any remaining placeholders\n"
            "2. Start n8n: [cyan]n8n start[/cyan]\n"
            "3. Import workflows: [cyan]python scripts/workflow_importer.py[/cyan]\n"
            "4. Validate workflows: [cyan]npm run validate[/cyan]\n\n"
            "[bold]Documentation:[/bold]\n"
            "• Installation Guide: [cyan]docs/INSTALLATION.md[/cyan]\n"
            "• Workflow Guide: [cyan]docs/WORKFLOW_GUIDE.md[/cyan]\n"
            "• Troubleshooting: [cyan]docs/TROUBLESHOOTING.md[/cyan]\n\n"
            "[bold]Need help?[/bold] Check docs/FAQ.md or open an issue on GitHub.",
            title="Setup Complete",
            border_style="green"
        ))
    
    def run(self) -> None:
        """Run the setup wizard"""
        try:
            self.welcome()
            
            if not self.check_existing_env():
                return
            
            self.collect_api_keys()
            self.create_env_file()
            self.test_connections()
            self.display_next_steps()
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Setup cancelled by user.[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[red]Error during setup: {e}[/red]")
            sys.exit(1)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Interactive setup wizard for Smart-RAG-Chatbot')
    parser.add_argument('--test', action='store_true', help='Test mode (dry run)')
    parser.add_argument('--dir', default='.', help='Project directory')
    
    args = parser.parse_args()
    
    if args.test:
        console.print("[yellow]Running in test mode (no changes will be made)[/yellow]")
        return
    
    wizard = SetupWizard(args.dir)
    wizard.run()


if __name__ == "__main__":
    main()
