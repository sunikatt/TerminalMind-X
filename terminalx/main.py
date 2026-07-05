import typer
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Load env variables first
load_dotenv()

from terminalx.parsers.history_parser import parse_bash_history
from terminalx.memory.engine import init_memory, remember_data, ask_memory

app = typer.Typer(help="TerminalX - Your Terminal Never Forgets")
console = Console()

def run_async(coro):
    """Helper to run async functions in Typer (which is sync by default)."""
    return asyncio.run(coro)

@app.command()
def init():
    """Initialize the TerminalX engine and database connections."""
    console.print(Panel.fit("[bold blue]TerminalX Initialization[/bold blue]"))
    run_async(init_memory())

@app.command()
def remember(file_path: str = typer.Argument("~/.bash_history", help="Path to history or file")):
    """Ingest a history file into long-term memory."""
    try:
        # 1. Parse the history
        console.print(f"[yellow]Parsing {file_path}...[/yellow]")
        commands = parse_bash_history(file_path)
        console.print(f"[green]Found {len(commands)} valid commands.[/green]")
        
        # 2. Add to Cognee memory with a loading spinner
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Building Knowledge Graph (this may take a minute)...", total=None)
            success = run_async(remember_data(commands, dataset_name="terminal_history"))
            
        if success:
            console.print("[bold green]✔ Memory stored and graph updated successfully![/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]Failed to ingest file:[/bold red] {e}")

@app.command()
def ask(question: str):
    """Ask TerminalX a question about your history."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]Searching memory..."),
        transient=True,
    ) as progress:
        progress.add_task(description="Searching...", total=None)
        answer = run_async(ask_memory(question))
        
    console.print(Panel(answer, title="[bold magenta]TerminalX Response[/bold magenta]", border_style="magenta"))

if __name__ == "__main__":
    app()